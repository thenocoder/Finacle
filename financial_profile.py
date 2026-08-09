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
from models.financial_profile import FinancialProfile


financial_profile_bp = Blueprint(
    "financial_profile",
    __name__,
    url_prefix="/financial-profile"
)


# ==========================================================
# Financial Profile Wizard
# ==========================================================

@financial_profile_bp.route("/", methods=["GET", "POST"])
@login_required
def onboarding():

    profile = FinancialProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":

        if profile is None:
            profile = FinancialProfile(
                user_id=current_user.id
            )
            db.session.add(profile)

        # ---------------------------------------
        # Question 1
        # ---------------------------------------

        profile.risk_appetite = request.form.get(
            "risk_appetite",
            "Medium"
        )

        # ---------------------------------------
        # Question 2
        # ---------------------------------------

        profile.financial_goal = request.form.get(
            "financial_goal",
            "Wealth Creation"
        )

        # ---------------------------------------
        # Question 3
        # ---------------------------------------

        profile.investment_horizon = request.form.get(
            "investment_horizon",
            "5+ Years"
        )

        # ---------------------------------------
        # Question 4
        # ---------------------------------------

        profile.emergency_fund_available = (
            request.form.get("emergency_fund") == "yes"
        )

        # ---------------------------------------
        # Question 5
        # ---------------------------------------

        investments = request.form.getlist(
            "investments"
        )

        profile.sip = "sip" in investments
        profile.stocks = "stocks" in investments
        profile.mutual_funds = "mutual_funds" in investments
        profile.gold = "gold" in investments
        profile.ppf = "ppf" in investments
        profile.nps = "nps" in investments
        profile.fd = "fd" in investments
        profile.lic = "lic" in investments

        db.session.commit()

        flash(
            "Financial Profile saved successfully.",
            "success"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    return render_template(

        "financial_profile/onboarding.html",

        profile=profile

    )


# ==========================================================
# View Profile
# ==========================================================

@financial_profile_bp.route("/view")
@login_required
def view_profile():

    profile = FinancialProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    if profile is None:

        return redirect(
            url_for(
                "financial_profile.onboarding"
            )
        )

    return render_template(

        "financial_profile/profile.html",

        profile=profile

    )