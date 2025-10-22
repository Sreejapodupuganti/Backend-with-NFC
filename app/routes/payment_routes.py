from flask import Blueprint, request, current_app, jsonify
from ..extensions import db
from ..models import User, Payment, Card, AnalyticsEvent
from ..services.payment_service import cashfree_create_order, verify_cashfree_webhook
from ..utils.security import auth_required
from ..utils.helpers import ok, bad
import random

payment_bp = Blueprint('payment', __name__)


@payment_bp.post("/create-order")
@auth_required
def create_order(user):
    data = request.get_json(force=True)
    amount = int(data.get('amount', 0))
    if amount <= 0:
        return bad('Invalid amount', 400)

    if not user.phone or not user.email or not user.name:
        return bad("Missing profile information!", 400)
    
    payment = Payment(user_id=user.id, amount=amount, status="PENDING")
    db.session.add(payment)
    db.session.flush()

    order_id = f"ORD_{user.id}_{payment.id + random.randint(1, 99999)}"
    cf_resp = cashfree_create_order(
        order_id=order_id,
        amount=amount,
        currency="INR",
        customer_id=str(user.id),
        customer_email=user.email,
        customer_phone=user.phone,
        return_url=data.get('return_url')
    )

    if not cf_resp.get("payment_session_id") and not cf_resp.get("payment_link"):
        db.session.rollback()
        return bad('failed to create cashfree order', 502)
    
    return ok({
        "order_id": order_id,
        "payment_link": cf_resp.get("payment_link"),
        "payment_session_id": cf_resp.get("payment_session_id"),
        "error": jsonify(cf_resp)
    })


@payment_bp.post("/webhook")
def cashfree_webhook():
    payload = request.get_data()
    headers = request.headers
    if not verify_cashfree_webhook(payload, headers):
        return bad("invalid signature", 401)

    data = request.get_json(force=True)
    order_id = data.get("data", {}).get("order", {}).get("order_id")
    payment_status = data.get("data", {}).get("payment", {}).get("payment_status")
    cf_payment_id = data.get("data", {}).get("payment", {}).get("payment_id")

    if not order_id:
        return bad("missing order_id", 400)

    payment = Payment.query.filter_by(order_id=order_id).first()
    if not payment:
        return bad("payment not found", 404)

    if payment_status == "SUCCESS":
        payment.status = "SUCCESS"
    elif payment_status in ("FAILED", "USER_DROPPED"):
        payment.status = "FAILED"
    else:
        payment.status = payment_status or "PENDING"
    payment.cf_payment_id = cf_payment_id
    db.session.commit()

    return ok({"message": "webhook processed"})

