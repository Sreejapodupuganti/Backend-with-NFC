import jwt
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
import datetime
# CONFIG
SERVICE_ACCOUNT_FILE = "app/config/serviceAccount.json"
SCOPES = ["https://www.googleapis.com/auth/wallet_object.issuer"]

# Load credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
authed_session = AuthorizedSession(credentials)

# Replace with your Issuer ID from Google Pay & Wallet Console
ISSUER_ID = "3388000000022985644"  # <-- CHANGE THIS

def create_generic_class():
    """Create the DigiCard class (only run once)"""
    url = "https://walletobjects.googleapis.com/walletobjects/v1/genericClass"
    payload = {
        "id": f"{ISSUER_ID}.digicardClass",
        "issuerName": "DigiCard",
        "reviewStatus": "UNDER_REVIEW",
        "hexBackgroundColor": "#5856D6",
        "cardTitle": {
            "defaultValue": {
                "language": "en-US",
                "value": "DIGI"   # <-- this text will appear instead of a logo
            }
        }
    }
    response = authed_session.post(url, json=payload)
    return response.json()



def create_generic_object(handle: str, title: str, designation: str, company: str, link: str):
    """Create a DigiCard object for a user"""
    url = "https://walletobjects.googleapis.com/walletobjects/v1/genericObject"
    object_id = f"{ISSUER_ID}.digicard-{handle}"
    
    # First check if object already exists
    response = authed_session.get(f"https://walletobjects.googleapis.com/walletobjects/v1/genericObject/{object_id}")

    if response.status_code == 200:
        return response.json()
    
    payload = {
        "id": object_id,
        "classId": f"3388000000022985644.3388000000022985644.digicardClass",
        "cardTitle": {
            "defaultValue": {"language": "en-US", "value": "DigiCard"}
        },
        "header": {
            "defaultValue": {"language": "en-US", "value": title}
        },
        "subheader": {
            "defaultValue": {"language": "en-US", "value": f"{designation} @ {company}"}
        },
        "barcode": {"type": "QR_CODE", "value": link},
        "linksModuleData": {
            "uris": [{"uri": link, "description": "View DigiCard"}]
        }
    }

    response = authed_session.post(url, json=payload)
    return response.json()

def generate_save_url(object_id: str):
    """Generate a Save-to-Google-Wallet URL for the given object"""
    issued_at = datetime.datetime.utcnow()
    expires_at = issued_at + datetime.timedelta(hours=1)

    claims = {
        "iss": credentials.service_account_email,
        "aud": "google",
        "typ": "savetowallet",
        "iat": issued_at,
        "exp": expires_at,
        "payload": {
            "genericObjects": [
                {"id": object_id}
            ]
        }
    }

    signed_jwt = jwt.encode(claims, credentials.signer._key, algorithm="RS256")
    return f"https://pay.google.com/gp/v/save/{signed_jwt}"

def tempCall():
    url = f"https://walletobjects.googleapis.com/walletobjects/v1/genericClass?issuerId={ISSUER_ID}"
    response = authed_session.get(url)
    print(response.status_code, response.json())
    return response.json()
