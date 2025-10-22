import hmac
import hashlib
import json
import requests
from flask import current_app


def cashfree_headers():
    return {
        "x-client-id": current_app.config["CASHFREE_CLIENT_ID"],
        "x-client-secret": current_app.config["CASHFREE_CLIENT_SECRET"],
        "x-api-version": "2023-08-01",
        "Content-Type": "application/json",
    }


def cashfree_create_order(order_id, amount, currency, customer_id, customer_email, customer_phone, return_url):
    base = current_app.config["CASHFREE_BASE_URL"].rstrip("/")
    url = f"{base}/orders"

    payload = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": currency,
        "customer_details": {
            "customer_id": customer_id,
            "customer_email": customer_email,
            "customer_phone": customer_phone
        },
        "order_meta":{
            'return_url': return_url
        }
    }

    resp = requests.post(url, headers=cashfree_headers(), data=json.dumps(payload), timeout=20)
    try:
        data = resp.json()
    except Exception:
        data = {}

    if resp.status_code in (200, 201):
        return {
            "payment_session_id": data.get("payment_session_id"),
            "payment_link": data.get("payment_link")
        }

    current_app.logger.error(f"Cashfree order error: {resp.status_code} {data}")
    return {}


def verify_cashfree_webhook(raw_body: bytes, headers) -> bool:
    secret = (current_app.config.get("CASHFREE_CLIENT_SECRET") or "").encode()
    signature = headers.get("x-webhook-signature") or headers.get("X-Webhook-Signature")
    if not secret or not signature:
        return False
    digest = hmac.new(secret, raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)
