from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import func

from extensions import db
from models.transaction import Transaction
from services.simulator_engine import SimulatorEngine


simulator_bp = Blueprint(
    "simulator",
    __name__,
    url_prefix="/simulator"
)


# ==========================================================
# Future Financial Simulator
# ==========================================================

@simulator_bp.route("/", methods=["GET", "POST"])
@login_required
def dashboard():

    # ------------------------------------------------------
    # Monthly Income
    # ------------------------------------------------------

    monthly_income = db.session.query(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "Income"
    ).scalar()

    # ------------------------------------------------------
    # Monthly Expense
    # ------------------------------------------------------

    monthly_expense = db.session.query(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "Expense"
    ).scalar()

    monthly_income = float(monthly_income or 0)
    monthly_expense = float(monthly_expense or 0)

    # ------------------------------------------------------
    # Default Values
    # ------------------------------------------------------

    monthly_investment = max(
        monthly_income - monthly_expense,
        0
    )

    annual_return = 12.0
    years = 10

    # ------------------------------------------------------
    # Form Submission
    # ------------------------------------------------------

    if request.method == "POST":

        monthly_investment = float(
            request.form.get(
                "monthly_investment",
                monthly_investment
            )
        )

        annual_return = float(
            request.form.get(
                "annual_return",
                annual_return
            )
        )

        years = int(
            request.form.get(
                "years",
                years
            )
        )

    # ------------------------------------------------------
    # Run Simulator
    # ------------------------------------------------------

    engine = SimulatorEngine(
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        monthly_investment=monthly_investment,
        annual_return=annual_return,
        years=years
    )

    simulation = engine.simulate()

    # ------------------------------------------------------
    # Render Page
    # ------------------------------------------------------

    return render_template(
        "simulator/dashboard.html",
        simulation=simulation
    )