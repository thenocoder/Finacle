from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.transaction import Transaction

from services.expense_predictor import ExpensePredictor


prediction_bp = Blueprint(
    "prediction",
    __name__,
    url_prefix="/prediction"
)


@prediction_bp.route("/")
@login_required
def dashboard():

    transactions = (

        Transaction.query

        .filter_by(
            user_id=current_user.id
        )

        .order_by(Transaction.date.asc())

        .all()

    )

    predictor = ExpensePredictor(
        transactions
    )

    result = predictor.predict()

    return render_template(

        "prediction/dashboard.html",

        prediction=result

    )