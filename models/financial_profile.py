from datetime import datetime

from extensions import db


class FinancialProfile(db.Model):
    __tablename__ = "financial_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    # -----------------------------
    # User Preferences
    # -----------------------------

    risk_appetite = db.Column(
        db.String(20),
        nullable=False,
        default="Medium"
    )

    financial_goal = db.Column(
        db.String(50),
        nullable=False,
        default="Wealth Creation"
    )

    investment_horizon = db.Column(
        db.String(20),
        nullable=False,
        default="5+ Years"
    )

    # -----------------------------
    # Existing Investments
    # -----------------------------

    sip = db.Column(db.Boolean, default=False)
    stocks = db.Column(db.Boolean, default=False)
    mutual_funds = db.Column(db.Boolean, default=False)
    gold = db.Column(db.Boolean, default=False)
    ppf = db.Column(db.Boolean, default=False)
    nps = db.Column(db.Boolean, default=False)
    fd = db.Column(db.Boolean, default=False)
    lic = db.Column(db.Boolean, default=False)

    # -----------------------------
    # Additional Information
    # -----------------------------

    emergency_fund_available = db.Column(
        db.Boolean,
        default=False
    )

    emergency_fund_months = db.Column(
        db.Integer,
        default=0
    )

    monthly_other_income = db.Column(
        db.Float,
        default=0
    )

    dependents = db.Column(
        db.Integer,
        default=0
    )

    # -----------------------------
    # Timestamps
    # -----------------------------

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # -----------------------------
    # Relationship
    # -----------------------------

    user = db.relationship(
        "User",
        backref=db.backref(
            "financial_profile",
            uselist=False
        )
    )

    def __repr__(self):
        return f"<FinancialProfile User={self.user_id}>"
