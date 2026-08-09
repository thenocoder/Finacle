from flask import Flask, redirect, url_for, render_template
from flask_login import current_user

from config import Config
from extensions import db, login_manager, migrate


# ==========================================================
# Models
# ==========================================================

from models.user import User
from models.transaction import Transaction
from models.ai_history import AIHistory
from models.financial_profile import FinancialProfile


# ==========================================================
# Blueprints
# ==========================================================

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.transactions import transaction_bp
from routes.csv_upload import csv_bp
from routes.ai import ai_bp
from routes.reports import reports_bp
from routes.settings import settings_bp

from routes.financial_profile import financial_profile_bp
from routes.allocation import allocation_bp
from routes.prediction import prediction_bp
from routes.simulator import simulator_bp


# ==========================================================
# Application Factory
# ==========================================================

def create_app():

    app = Flask(__name__)

    # ======================================================
    # Configuration
    # ======================================================

    app.config.from_object(Config)

    # ======================================================
    # Initialize Extensions
    # ======================================================

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # ======================================================
    # Flask Login
    # ======================================================

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to continue."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(
            User,
            int(user_id)
        )

    # ======================================================
    # Register Blueprints
    # ======================================================

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(csv_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(settings_bp)

    # ======================================================
    # Finacle Modules
    # ======================================================

    app.register_blueprint(financial_profile_bp)
    app.register_blueprint(allocation_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(simulator_bp)

    # ======================================================
    # Home Route
    # ======================================================

    @app.route("/")
    def home():

        if current_user.is_authenticated:

            return redirect(
                url_for("dashboard.dashboard")
            )

        return redirect(
            url_for("auth.login")
        )

    # ======================================================
    # Error Handlers
    # ======================================================

    @app.errorhandler(404)
    def page_not_found(error):

        return render_template(
            "errors/404.html"
        ), 404

    @app.errorhandler(500)
    def internal_server_error(error):

        db.session.rollback()

        return render_template(
            "errors/500.html"
        ), 500

    # ======================================================
    # Create Database
    # ======================================================

    with app.app_context():

        db.create_all()

    return app


# ==========================================================
# Run Application
# ==========================================================

app = create_app()

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )