from datetime import datetime

from extensions import db


class AIHistory(db.Model):
    __tablename__ = "ai_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    analysis_type = db.Column(
        db.String(100),
        nullable=False
    )

    prompt = db.Column(
        db.Text,
        nullable=False
    )

    response = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )