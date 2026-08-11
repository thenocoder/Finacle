from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
import os

csv_bp = Blueprint("csv", __name__)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@csv_bp.route("/csv/upload", methods=["GET", "POST"])
@login_required
def upload_csv():

    if request.method == "POST":

        if "file" not in request.files:
            flash("No file selected.", "danger")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("Please choose a CSV file.", "warning")
            return redirect(request.url)

        if file and allowed_file(file.filename):

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            file.save(filepath)

            return redirect(
                url_for("csv.preview_csv", filename=filename)
            )

        flash("Only CSV files are allowed.", "danger")

    return render_template("csv/upload.html")


@csv_bp.route("/csv/preview/<filename>")
@login_required
def preview_csv(filename):

    return render_template(
        "csv/preview.html",
        filename=filename
    )