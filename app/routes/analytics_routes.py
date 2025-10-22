from flask import Blueprint, request
from ..extensions import db
from ..models import Card, AnalyticsEvent
from ..utils.helpers import ok, bad

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.post("/track")
def track_event():
    data = request.get_json(force=True)
    handle = data.get("handle")
    event_type = data.get("event_type", "profile_view")
    meta = data.get("meta", "{}")

    card = Card.query.filter_by(handle=handle).first()
    if not card:
        return bad("card not found", 404)

    ev = AnalyticsEvent(card_id=card.id, event_type=event_type, meta=meta)
    db.session.add(ev)
    db.session.commit()
    return ok({"message": "tracked"})