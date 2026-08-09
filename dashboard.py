from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from datetime import datetime
from services.dashboard_analytics import DashboardAnalytics
from models.transaction import Transaction

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@login_required
def dashboard():

    # ============================
    # Total Income
    # ============================

    total_income = (
        Transaction.query.with_entities(
            func.sum(Transaction.amount)
        )
        .filter_by(
            user_id=current_user.id,
            type="Income"
        )
        .scalar()
        or 0
    )

    # ============================
    # Total Expense
    # ============================

    total_expense = (
        Transaction.query.with_entities(
            func.sum(Transaction.amount)
        )
        .filter_by(
            user_id=current_user.id,
            type="Expense"
        )
        .scalar()
        or 0
    )

    # ============================
    # Balance
    # ============================

    balance = total_income - total_expense

    # ============================
    # Savings %
    # ============================

    savings_percentage = 0

    if total_income > 0:
        savings_percentage = (
            balance / total_income
        ) * 100

    # ============================
    # Total Transactions
    # ============================

    total_transactions = (
        Transaction.query
        .filter_by(user_id=current_user.id)
        .count()
    )

    # ============================
    # This Month Expense
    # ============================

    current_month = datetime.now().month
    current_year = datetime.now().year

    this_month_expense = (
        Transaction.query.with_entities(
            func.sum(Transaction.amount)
        )
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "Expense",
            extract("month", Transaction.date) == current_month,
            extract("year", Transaction.date) == current_year
        )
        .scalar()
        or 0
    )

    # ============================
    # Recent Transactions
    # ============================

    recent_transactions = (
        Transaction.query
        .filter_by(user_id=current_user.id)
        .order_by(Transaction.date.desc())
        .limit(5)
        .all()
    )

    # ============================
    # Expense Category Data
    # ============================

    category_data = (
        Transaction.query.with_entities(
            Transaction.category,
            func.sum(Transaction.amount)
        )
        .filter_by(
            user_id=current_user.id,
            type="Expense"
        )
        .group_by(Transaction.category)
        .all()
    )

    category_labels = [
        item[0] for item in category_data
    ]

    category_amounts = [
        float(item[1]) for item in category_data
    ]

    # ============================
    # Top Spending Category
    # ============================

    top_category = "N/A"

    if category_data:

        highest = max(
            category_data,
            key=lambda x: x[1]
        )

        top_category = highest[0]

    # ============================
    # Monthly Income
    # ============================

    income_data = (
        Transaction.query.with_entities(
            extract("month", Transaction.date),
            func.sum(Transaction.amount)
        )
        .filter_by(
            user_id=current_user.id,
            type="Income"
        )
        .group_by(
            extract("month", Transaction.date)
        )
        .all()
    )

    # ============================
    # Monthly Expense
    # ============================

    expense_data = (
        Transaction.query.with_entities(
            extract("month", Transaction.date),
            func.sum(Transaction.amount)
        )
        .filter_by(
            user_id=current_user.id,
            type="Expense"
        )
        .group_by(
            extract("month", Transaction.date)
        )
        .all()
    )

    month_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    monthly_income = [0] * 12
    monthly_expense = [0] * 12

    for month, amount in income_data:
        monthly_income[int(month) - 1] = float(amount)

    for month, amount in expense_data:
        monthly_expense[int(month) - 1] = float(amount)

    # ============================
    # Dashboard Analytics
    # ============================

    dashboard_analytics = DashboardAnalytics(

        income=total_income,

        expense=total_expense,

        transactions=total_transactions

    ).generate()

    # ============================
    # Render Dashboard
    # ============================

    return render_template(

        "dashboard/dashboard.html",

        user=current_user,

        total_income=round(total_income, 2),

        total_expense=round(total_expense, 2),

        balance=round(balance, 2),

        savings_percentage=round(savings_percentage, 2),

        total_transactions=total_transactions,

        this_month_expense=round(this_month_expense, 2),

        top_category=top_category,

        recent_transactions=recent_transactions,

        month_labels=month_names,

        monthly_income=monthly_income,

        monthly_expense=monthly_expense,

        category_labels=category_labels,

        category_amounts=category_amounts,
          dashboard=dashboard_analytics

    )