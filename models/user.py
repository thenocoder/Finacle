from datetime import datetime

from flask_login import UserMixin

from extensions import db, login_manager


# ==========================================================
# User Model
# ==========================================================

class User(UserMixin, db.Model):
    __tablename__ = "users"

    # ======================================================
    # Primary Key
    # ======================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ======================================================
    # User Information
    # ======================================================

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ======================================================
    # Relationships
    # ======================================================

    transactions = db.relationship(
        "Transaction",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    ai_history = db.relationship(
        "AIHistory",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ======================================================
    # String Representation
    # ======================================================

    def __repr__(self):
        return f"<User {self.email}>"


# ==========================================================
# Flask-Login User Loader
# ==========================================================

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
