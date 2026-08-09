"""
=========================================================
Finacle Reports Routes
=========================================================

Responsibilities
----------------
• Reports Dashboard
• PDF Generation
• PDF Download
• Report Summary API
• Debug API
• Health Check

Architecture
------------
Routes
    ↓
ReportDataService
    ↓
ReportGenerator
    ↓
PDF Response

This module contains NO business logic.
It only coordinates HTTP requests.
"""

from __future__ import annotations

import logging

from typing import Any

from flask import (

    Blueprint,

    abort,

    current_app,

    flash,

    jsonify,

    redirect,

    render_template,

    send_file,

    url_for,

)

from flask_login import (

    current_user,

    login_required,

)

from services.report_data import (
    ReportDataService,
)

from services.report_generator import (
    ReportGenerator,
)


logger = logging.getLogger(__name__)

# ==========================================================
# BLUEPRINT
# ==========================================================

reports_bp = Blueprint(

    "reports",

    __name__,

    url_prefix="/reports",

)

# ==========================================================
# INTERNAL HELPERS
# ==========================================================

def _build_report_data() -> dict[str, Any]:
    """
    Build the complete report dataset
    for the authenticated user.
    """

    if not current_user.is_authenticated:

        raise PermissionError(
            "Authentication required."
        )

    logger.info(

        "Building report dataset for user %s",

        current_user.id,

    )

    service = ReportDataService(
        current_user.id
    )

    report_data = service.build_report()

    if not isinstance(
        report_data,
        dict,
    ):

        raise RuntimeError(

            "ReportDataService.build_report() "

            "must return a dictionary."

        )

    logger.info(
        "Report dataset built successfully."
    )

    return report_data


# ---------------------------------------------------------

def _create_generator() -> ReportGenerator:
    """
    Create a synchronized ReportGenerator.
    """

    logger.info(

        "Creating ReportGenerator for user %s",

        current_user.id,

    )

    return ReportGenerator(
        current_user.id
    )


# ---------------------------------------------------------

def _handle_exception(
    exc: Exception,
    message: str,
):

    logger.exception(message)

    flash(
        message,
        "danger",
    )

    return redirect(
        url_for(
            "dashboard.dashboard"
        )
    )

# ==========================================================
# REPORT DASHBOARD
# ==========================================================
# ==========================================================
# REPORT DASHBOARD
# ==========================================================

@reports_bp.route("/")
@login_required
def dashboard():
    """
    Render the Reports Dashboard.
    """

    try:

        report_data = _build_report_data()

        logger.info(

            "Reports dashboard rendered successfully for user %s",

            current_user.id,

        )

        return render_template(

            "reports/dashboard.html",

            **report_data,

        )
    except Exception as exc:
         raise
        

   
   
    

# ==========================================================
# GENERATE PDF
# ==========================================================
# ==========================================================
# GENERATE PDF
# ==========================================================

@reports_bp.route("/generate")
@login_required
def generate_pdf():
    """
    Generate and immediately download
    the user's financial report.
    """

    try:

        logger.info(

            "Starting PDF generation for user %s",

            current_user.id,

        )

        generator = _create_generator()

        pdf_path = generator.generate()

        logger.info(

            "PDF generated successfully for user %s",

            current_user.id,

        )

        return send_file(

            pdf_path,

            mimetype="application/pdf",

            as_attachment=True,

            download_name=pdf_path.name,

            max_age=0,

        )

    except Exception as exc:

        logger.exception(

            "PDF generation failed for user %s",

            current_user.id,

        )

        flash(

            f"Unable to generate report: {exc}",

            "danger",

        )

        return redirect(

            url_for(
                "reports.dashboard"
            )

        )

# ==========================================================
# DOWNLOAD EXISTING REPORT
# ==========================================================

@reports_bp.route("/download")
@login_required
def download_latest():
    """
    Generate a fresh report and
    return it as a downloadable PDF.
    """

    try:

        generator = _create_generator()

        pdf_path = generator.generate()

        return send_file(

            pdf_path,

            as_attachment=True,

            download_name=pdf_path.name,

            mimetype="application/pdf",

            max_age=0,

        )

    except Exception as exc:

        logger.exception(

            "Report download failed for user %s",

            current_user.id,

        )

        flash(

            "Unable to download report.",

            "danger",

        )

        return redirect(

            url_for(
                "reports.dashboard"
            )

        )

# ==========================================================
# DEBUG ENDPOINT
# ==========================================================
# ==========================================================
# DEBUG ENDPOINT
# ==========================================================

@reports_bp.route("/debug")
@login_required
def debug():
    """
    Return the complete report dataset.

    Available only while Flask
    is running in debug mode.
    """

    if not current_app.debug:

        abort(404)

    try:

        report_data = _build_report_data()

        logger.info(

            "Debug endpoint accessed by user %s",

            current_user.id,

        )

        return jsonify(

            success=True,

            user_id=current_user.id,

            report=report_data,

        )

    except Exception as exc:

        logger.exception(

            "Debug endpoint failed for user %s",

            current_user.id,

        )

        return jsonify(

            success=False,

            error=str(exc),

        ), 500


# ==========================================================
# REPORT SUMMARY API
# ==========================================================

@reports_bp.route("/summary")
@login_required
def summary():
    """
    Return a lightweight report summary.
    """

    try:

        service = ReportDataService(
            current_user.id
        )

        summary_data = service.report_summary()

        if not isinstance(
            summary_data,
            dict,
        ):

            raise RuntimeError(

                "report_summary() must return a dictionary."

            )

        logger.info(

            "Summary returned successfully for user %s",

            current_user.id,

        )

        return jsonify(

            success=True,

            summary=summary_data,

        )

    except Exception as exc:

        logger.exception(

            "Unable to build report summary for user %s",

            current_user.id,

        )

        return jsonify(

            success=False,

            error=str(exc),

        ), 500


# ==========================================================
# HEALTH CHECK
# ==========================================================
# ==========================================================
# HEALTH CHECK
# ==========================================================

@reports_bp.route("/health")
def health():
    """
    Reporting module health endpoint.
    """

    try:

        authenticated = bool(
            current_user.is_authenticated
        )

    except Exception:

        authenticated = False

    return jsonify(

        success=True,

        service="Finacle Reporting",

        blueprint="reports",

        version="5.0",

        status="OK",

        authenticated=authenticated,

    )


# ==========================================================
# ROUTE INFORMATION
# ==========================================================

@reports_bp.route("/info")
def info():
    """
    Return reporting module information.
    """

    return jsonify(

        success=True,

        module="Finacle Reporting",

        version="5.0",

        routes={

            "dashboard": "/reports/",

            "generate_pdf": "/reports/generate",

            "download_pdf": "/reports/download",

            "summary": "/reports/summary",

            "debug": "/reports/debug",

            "health": "/reports/health",

        },

    )


# ==========================================================
# END OF FILE
# ==========================================================
