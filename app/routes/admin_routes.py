from flask import Blueprint
from sqlalchemy import func
from ..models import User, Payment, AnalyticsEvent
from ..utils.security import admin_required
from ..utils.helpers import ok

admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/overview")
@admin_required
def overview(admin_user):
    users_count = User.query.count()
    total_revenue = (Payment.query.with_entities(func.coalesce(func.sum(Payment.amount), 0))
                     .filter_by(status="SUCCESS").scalar())
    payments = Payment.query.order_by(Payment.created_at.desc()).limit(25).all()
    events = AnalyticsEvent.query.order_by(AnalyticsEvent.occurred_at.desc()).limit(25).all()

    return ok({
        "users": users_count,
        "total_revenue": int(total_revenue or 0),
        "recent_payments": [
            {"order_id": p.order_id, "amount": p.amount, "status": p.status, "created_at": p.created_at.isoformat()}
            for p in payments
        ],
        "recent_events": [
            {"type": e.event_type, "at": e.occured_at.isoformat()}
            for e in events
        ]
    })
