from flask import Blueprint, request
from ..extensions import db
from ..models import Card
from ..utils.security import auth_required
from ..utils.helpers import ok, bad
import json

card_bp = Blueprint('card', __name__)


@card_bp.get("/public/<handle>")
def get_public_card(handle):
    card = Card.query.filter_by(handle=handle).first()
    if not card:
        return bad("card not found",404)

    return ok({
        "handle": card.handle,
        "title": card.title,
        "company": card.company,
        "phone": card.user.phone,
        "designation": card.designation,
        "bio": card.bio,
        "avatar_url": card.avatar_url,
        "theme": card.theme,
        "links": json.loads(card.links_json or "[]"),
        "user_public_id": card.user.public_id
    })


@card_bp.put("/me")
@auth_required
def update_my_card(user):
    data = request.get_json()
    card = user.card
    if not card:
        return bad("card not found", 404)

    fields = ["title", "company", "designation", "bio", "avatar_url", "theme"]
    for f in fields:
        if f in data:
            setattr(card, f, data[f])

    card.user.phone = data["phone"]

    if "links" in data and isinstance(data["links"], list):
        card.links_json = json.dumps(data["links"])

    db.session.commit()
    return ok({"message" : "updated", "handle": card.handle})


@card_bp.get("/me")
@auth_required
def my_card(user):
    card = user.card
    return ok({
        "handle": card.handle,
        "title": card.title,
        "company": card.company,
        "designation": card.designation,
        "bio": card.bio,
        "avatar_url": card.avatar_url,
        "theme": card.theme,
        "links": json.loads(card.links_json or "[]")
    })