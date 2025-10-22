from datetime import datetime
from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    card = db.relationship("Card", backref="user", uselist=False, cascade="all, delete-orphan")


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(120))
    company = db.Column(db.String(120))
    designation = db.Column(db.String(120))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    theme = db.Column(db.String(40), default="light")
    links_json = db.Column(db.Text, default="[]")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), default="INR")
    status = db.Column(db.String(20), default="PENDING")
    order_id = db.Column(db.String(64), unique=True)
    cf_payment_id = db.Column(db.String(64))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AnalyticsEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    event_type = db.Column(db.String(40))
    meta = db.Column(db.Text)
    occurred_at = db.Column(db.DateTime, default=datetime.utcnow)

    card = db.relationship("Card", backref=db.backref("events", lazy=True))