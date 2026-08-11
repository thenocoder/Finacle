import os
import pandas as pd

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
    session
)

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from extensions import db
from models.transaction import Transaction

csv_bp = Blueprint("csv", __name__, url_prefix="/csv")

ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def prepare_dataframe(df):
    """
    Convert different CSV formats into Finacle's standard format.
    """

    column_mapping = {
        "Expense Date": "Date",
        "Transaction Date": "Date",
        "Description": "Notes",
        "Remark": "Notes",
        "Remarks": "Notes",
        "PaymentMethod": "Payment Method",
    }

    df = df.rename(columns=column_mapping)

    # If Type doesn't exist, assume all transactions are Expenses
    if "Type" not in df.columns:
        df["Type"] = "Expense"

    # If Notes column doesn't exist
    if "Notes" not in df.columns:
        df["Notes"] = ""

    return df


@csv_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_csv():

    if request.method == "POST":

        if "file" not in request.files:
            flash("Please choose a CSV file.", "danger")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("Please choose a CSV file.", "warning")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Only CSV files are allowed.", "danger")
            return redirect(request.url)

        upload_folder = os.path.join(
            current_app.root_path,
            current_app.config["UPLOAD_FOLDER"]
        )

        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(file.filename)

        filepath = os.path.join(upload_folder, filename)

        file.save(filepath)

        try:

            df = pd.read_csv(filepath)

            df = prepare_dataframe(df)

        except Exception as e:

            flash(f"Unable to read CSV: {e}", "danger")
            return redirect(request.url)

        required_columns = [
            "Date",
            "Type",
            "Title",
            "Category",
            "Amount",
            "Payment Method",
            "Notes"
        ]

        missing_columns = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:

            flash(
                "Missing columns: " + ", ".join(missing_columns),
                "danger"
            )

            return redirect(request.url)

        session["csv_file"] = filepath

        preview = df.head(10).to_dict(orient="records")

        return render_template(
            "csv/preview.html",
            rows=preview,
            columns=df.columns.tolist(),
            total_rows=len(df)
        )

    return render_template("csv/upload.html")


@csv_bp.route("/import", methods=["POST"])
@login_required
def import_csv():

    filepath = session.get("csv_file")

    if not filepath:

        flash("No uploaded CSV found.", "warning")
        return redirect(url_for("csv.upload_csv"))

    try:

        df = pd.read_csv(filepath)

        df = prepare_dataframe(df)

        imported = 0
        skipped = 0

        for _, row in df.iterrows():

            try:

                transaction_date = pd.to_datetime(
                    row["Date"]
                ).date()

                # Check duplicate transaction
                existing = Transaction.query.filter_by(
                    user_id=current_user.id,
                    title=str(row["Title"]).strip(),
                    amount=float(row["Amount"]),
                    date=transaction_date,
                    type=str(row["Type"]).strip()
                ).first()

                if existing:
                    skipped += 1
                    continue

                transaction = Transaction(

                    user_id=current_user.id,

                    type=str(row["Type"]).strip(),

                    title=str(row["Title"]).strip(),

                    category=str(row["Category"]).strip(),

                    amount=float(row["Amount"]),

                    payment_method=str(row["Payment Method"]).strip(),

                    date=transaction_date,

                    notes="" if pd.isna(row["Notes"]) else str(row["Notes"])

                )

                db.session.add(transaction)

                imported += 1

            except Exception:
                skipped += 1

        db.session.commit()

        session.pop("csv_file", None)

        flash(
            f"Import Completed! "
            f"{imported} imported, "
            f"{skipped} skipped.",
            "success"
        )

        return redirect(url_for("dashboard.dashboard"))

    except Exception as e:

        db.session.rollback()

        flash(f"Import failed: {e}", "danger")

        return redirect(url_for("csv.upload_csv"))