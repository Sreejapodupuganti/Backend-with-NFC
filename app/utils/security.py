import time
import jwt
from functools import wraps
from flask import request
from ..models import User
from ..extensions import db
from flask import current_app
from ..utils.helpers import bad


def create_jwt(user: User, ttl_seconds: int = 60 * 60 * 24 * 7) -> str:
    payload = {
        "sub": user.public_id,
        "iss": current_app.config["JWT_ISSUER"],
        "iat": int(time.time()),
        "exp": int(time.time()) + ttl_seconds,
        "admin": user.is_admin
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")

def decode_jwt(token: str):
    return jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"], issuer=current_app.config["JWT_ISSUER"])

def _get_bearer_token():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth.split(" ", 1)[1].strip()
    return None

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _get_bearer_token()
        if not token:
            return bad("missing bearer token", 401)
        try:
            payload = decode_jwt(token)
        except Exception as e:
            return bad(f"Invalid Token: {e}", 401)
        user = User.query.filter_by(public_id=payload.get("sub")).first()
        if not user:
            return bad("user not found", 404)
        return fn(user, *args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _get_bearer_token()
        if not token:
            return bad("missing bearer token", 401)
        try:
            payload = decode_jwt(token)
        except Exception as e:
            return bad("admin only", 403)
        if not payload.get("admin"):
            return bad("admin only", 403)

        user = User.query.filter_by(public_id=payload.get("sub")).first()
        if not user:
            return bad("user not found", 404)
        return fn(user, *args, **kwargs)
    return wrapper


