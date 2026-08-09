from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db



transaction_bp = Blueprint(
    "transactions",
    __name__,
    url_prefix="/transactions"
)


# ===========================
# View All Transactions
# ===========================

@transaction_bp.route("/")
@login_required
def transactions():

    transaction_list = (
        Transaction.query
        .filter_by(user_id=current_user.id)
        .order_by(Transaction.date.desc())
        .all()
    )

    return render_template(
        "transactions/transactions.html",
        transactions=transaction_list
    )


# ===========================
# Add Transaction
# ===========================

@transaction_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_transaction():

    if request.method == "POST":

        transaction = Transaction(

            user_id=current_user.id,

            type=request.form["type"],

            title=request.form["title"],

            category=request.form["category"],

            amount=float(request.form["amount"]),

            payment_method=request.form["payment_method"],

            date=datetime.strptime(
                request.form["date"],
                "%Y-%m-%d"
            ).date(),

            notes=request.form.get("notes")

        )

        db.session.add(transaction)
        db.session.commit()

        flash(
            "Transaction added successfully.",
            "success"
        )

        return redirect(
            url_for("transactions.transactions")
        )

    return render_template(
        "transactions/add_transaction.html"
    )


# ===========================
# Edit Transaction
# ===========================

@transaction_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_transaction(id):

    transaction = Transaction.query.get_or_404(id)

    if transaction.user_id != current_user.id:

        flash(
            "Unauthorized access.",
            "danger"
        )

        return redirect(
            url_for("transactions.transactions")
        )

    if request.method == "POST":

        transaction.type = request.form["type"]

        transaction.title = request.form["title"]

        transaction.category = request.form["category"]

        transaction.amount = float(
            request.form["amount"]
        )

        transaction.payment_method = request.form[
            "payment_method"
        ]

        transaction.date = datetime.strptime(
            request.form["date"],
            "%Y-%m-%d"
        ).date()

        transaction.notes = request.form.get("notes")

        db.session.commit()

        flash(
            "Transaction updated successfully.",
            "success"
        )

        return redirect(
            url_for("transactions.transactions")
        )

    return render_template(
        "transactions/edit_transaction.html",
        transaction=transaction
    )


# ===========================
# Delete Transaction
# ===========================

@transaction_bp.route("/delete/<int:id>")
@login_required
def delete_transaction(id):

    transaction = Transaction.query.get_or_404(id)

    if transaction.user_id != current_user.id:

        flash(
            "Unauthorized access.",
            "danger"
        )

        return redirect(
            url_for("transactions.transactions")
        )

    db.session.delete(transaction)
    db.session.commit()

    flash(
        "Transaction deleted successfully.",
        "success"
    )

    return redirect(
        url_for("transactions.transactions")
    )
