from flask import Blueprint, request
from uuid import uuid4
from ..extensions import db, bcrypt
from ..models import User, Card
from ..utils.security import create_jwt
from ..utils.helpers import ok, bad

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(force=True)
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    name = data.get("name", "")

    if not email or not password or not name:
        return bad("name, email, password are required", 400)

    if User.query.filter_by(email=email).first():
        return bad("email already registered", 400)


    user = User(
        public_id=str(uuid4()),
        email=email,
        password_hash=bcrypt.generate_password_hash(password).decode("utf8"),
        name=name
    )
    db.session.add(user)
    db.session.flush()

    handle = email.split("@")[0]
    if Card.query.filter_by(handle=handle).first():
        handle = f"{handle}-{user.id}"

    card = Card(handle=handle, user_id=user.id, title=name)
    db.session.add(card)
    db.session.commit()

    token =create_jwt(user)
    return ok({"token": token, "user": {"public_id": user.public_id, "email": user.email, "handle": card.handle}})


@auth_bp.post("/login")
def login():
    data = request.get_json(force=True)
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return bad("invalid email or password", 400)

    token = create_jwt(user)

    return ok({"token": token, "user": {"public_id": user.public_id, "email": user.email, "is_admin": user.is_admin}})


