import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///business_card.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTO_CREATE_DB = True
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
    JWT_ISSUER = os.getenv("JWT_ISSUER", "digital-bizcard")

    CASHFREE_CLIENT_ID = os.getenv("CASHFREE_CLIENT_ID", "")
    CASHFREE_CLIENT_SECRET = os.getenv("CASHFREE_CLIENT_SECRET", "")
    CASHFREE_BASE_URL = os.getenv("CASHFREE_BASE_URL", "https://sandbox.cashfree.com/pg")
    CASHFREE_WEBHOOK_SECRET = os.getenv("CASHFREE_WEBHOOK_SECRET", "")

