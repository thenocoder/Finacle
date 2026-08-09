from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from sqlalchemy import func

from extensions import db

from models.financial_profile import FinancialProfile
from models.transaction import Transaction

from services.allocation_engine import AllocationEngine


allocation_bp = Blueprint(
    "allocation",
    __name__,
    url_prefix="/allocation"
)


# ==========================================================
# Smart Financial Allocation
# ==========================================================

@allocation_bp.route("/")
@login_required
def dashboard():

    # ------------------------------------------------------
    # Get Financial Profile
    # ------------------------------------------------------

    profile = FinancialProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    if profile is None:

        flash(
            "Please complete your Financial Profile first.",
            "warning"
        )

        return redirect(
            url_for("financial_profile.onboarding")
        )

    # ------------------------------------------------------
    # Total Income
    # ------------------------------------------------------

    total_income = db.session.query(

        func.coalesce(
            func.sum(Transaction.amount),
            0
        )

    ).filter(

        Transaction.user_id == current_user.id,
        Transaction.type == "Income"

    ).scalar()

    # ------------------------------------------------------
    # Total Expense
    # ------------------------------------------------------

    total_expense = db.session.query(

        func.coalesce(
            func.sum(Transaction.amount),
            0
        )

    ).filter(

        Transaction.user_id == current_user.id,
        Transaction.type == "Expense"

    ).scalar()

    # ------------------------------------------------------
    # Smart Allocation Engine
    # ------------------------------------------------------

    engine = AllocationEngine(

        monthly_income=float(total_income),

        monthly_expense=float(total_expense),

        profile=profile

    )

    result = engine.generate()

    # ------------------------------------------------------
    # Render Dashboard
    # ------------------------------------------------------

    return render_template(

        "allocation/dashboard.html",

        result=result,

        profile=profile,

        total_income=total_income,

        total_expense=total_expense

    )
