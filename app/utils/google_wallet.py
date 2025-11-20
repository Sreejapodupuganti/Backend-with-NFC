import jwt
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
import datetime
import os
import json

# ---------------------------
# SERVICE ACCOUNT CREDENTIALS
# ---------------------------

SCOPES = ["https://www.googleapis.com/auth/wallet_object.issuer"]

# Load JSON string from Azure App Settings
service_json = os.getenv("GOOGLE_SERVICE_JSON")

if not service_json:
    raise Exception(
        "GOOGLE_SERVICE_JSON is missing. Add it in Azure → Configuration → Application Settings."
    )

# Parse JSON string to dictionary
try:
    info = json.loads(service_json)
    credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
except Exception as e:
    raise Exception("Failed to load Google Wallet service account JSON.") from e

# Authorized session for Google Wallet API
authed_session = AuthorizedSession(credentials)

# Your Issuer ID from Google Wallet Console
ISSUER_ID = "3388000000022985644"


# -----------------------------------------------
# Create ID for data classes & objects
# -----------------------------------------------
def generate_data_class_id():
    return f"{ISSUER_ID}.businesscard_class_id"


def generate_data_object_id(username):
    return f"{ISSUER_ID}.{username.replace(' ', '_').lower()}_object"


# -----------------------------------------------
# Create Wallet Data Class
# -----------------------------------------------
def create_data_class():
    class_id = generate_data_class_id()

    data_class = {
        "id": class_id,
        "classTemplateInfo": {
            "cardTemplateOverride": {
                "cardRowTemplateInfos": [
                    {
                        "twoItems": {
                            "startItem": {"firstValue": {"fields": [{"fieldPath": "cardHolderName"}]}}
                        }
                    },
                    {
                        "twoItems": {
                            "startItem": {"firstValue": {"fields": [{"fieldPath": "company"}]}},
                            "endItem": {"firstValue": {"fields": [{"fieldPath": "jobTitle"}]}}
                        }
                    }
                ]
            }
        }
    }

    url = f"https://walletobjects.googleapis.com/walletobjects/v1/genericClass"
    response = authed_session.post(url, json=data_class)

    return response.status_code, response.json()


# -----------------------------------------------
# Create Wallet Data Object (Card)
# -----------------------------------------------
def create_data_object(username, email, company, job_title):
    object_id = generate_data_object_id(username)

    data_object = {
        "id": object_id,
        "classId": generate_data_class_id(),
        "cardHolderName": username,
        "textModulesData": [
            {"header": "Email", "body": email},
            {"header": "Company", "body": company},
            {"header": "Job Title", "body": job_title}
        ]
    }

    url = f"https://walletobjects.googleapis.com/walletobjects/v1/genericObject"
    response = authed_session.post(url, json=data_object)

    return response.status_code, response.json()


# -----------------------------------------------
# Generate Save-to-Google-Wallet Link
# -----------------------------------------------
def generate_save_link(username, email, company, job_title):
    object_id = generate_data_object_id(username)

    claims = {
        "iss": info["client_email"],
        "aud": "google",
        "typ": "savetowallet",
        "iat": datetime.datetime.utcnow(),
        "payload": {
            "genericObjects": [
                {
                    "id": object_id,
                    "classId": generate_data_class_id(),
                    "cardHolderName": username,
                    "textModulesData": [
                        {"header": "Email", "body": email},
                        {"header": "Company", "body": company},
                        {"header": "Job Title", "body": job_title}
                    ]
                }
            ]
        }
    }

    token = jwt.encode(claims, info["private_key"], algorithm="RS256")

    save_url = f"https://pay.google.com/gp/v/save/{token}"

    return save_url
