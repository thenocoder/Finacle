from flask import (
    Blueprint,
    render_template,
    request
)

from flask_login import (
    login_required,
    current_user
)

from sqlalchemy import func

from extensions import db

from models.income import Income
from models.transaction import Transaction

from services.future_financial_simulator import (
    FutureFinancialSimulator
)


future_simulator_bp = Blueprint(
    "future_simulator",
    __name__,
    url_prefix="/future-simulator"
)


@future_simulator_bp.route(
    "/",
    methods=["GET", "POST"]
)
@login_required
def dashboard():

    total_income = db.session.query(

        func.coalesce(
            func.sum(Income.amount),
            0
        )

    ).filter(

        Income.user_id == current_user.id

    ).scalar()

    total_expense = db.session.query(

        func.coalesce(
            func.sum(Transaction.amount),
            0
        )

    ).filter(

        Transaction.user_id == current_user.id,

        Transaction.type == "Expense"

    ).scalar()

    monthly_investment = 5000
    annual_return = 12
    salary_growth = 8
    inflation = 6
    years = 10

    if request.method == "POST":

        monthly_investment = float(

            request.form.get(
                "monthly_investment",
                5000
            )
        )

        annual_return = float(

            request.form.get(
                "annual_return",
                12
            )
        )

        salary_growth = float(

            request.form.get(
                "salary_growth",
                8
            )
        )

        inflation = float(

            request.form.get(
                "inflation",
                6
            )
        )

        years = int(

            request.form.get(
                "years",
                10
            )
        )

    simulator = FutureFinancialSimulator(

        monthly_income=total_income,

        monthly_expense=total_expense,

        monthly_investment=monthly_investment,

        annual_return=annual_return,

        salary_growth=salary_growth,

        inflation=inflation,

        years=years

    )

    simulation = simulator.simulate()

    return render_template(

        "simulator/dashboard.html",

        simulation=simulation

    )