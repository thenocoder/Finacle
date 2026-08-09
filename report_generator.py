"""
=========================================================
Finacle PDF Report Generator
=========================================================

Coordinates the complete PDF report generation process.

Pipeline

ReportDataService
        ↓
ReportCharts
        ↓
ReportPages
        ↓
Final PDF
"""

from __future__ import annotations

import logging

from datetime import datetime

from pathlib import Path

from typing import Any

from reportlab.pdfgen import canvas

from services.report_data import ReportDataService
from services.report_charts import ReportCharts
from services.report_pages import ReportPages


logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Coordinates the complete report
    generation pipeline.

    No financial calculations are
    performed inside this class.
    """

    DEFAULT_DIRECTORY = "reports"

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(
        self,
        user_id: int,
        output_directory: str | Path = DEFAULT_DIRECTORY,
    ) -> None:

        self.user_id = user_id

        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        self.report_data: dict[str, Any] = {}

        self.chart_paths: dict[str, str] = {}

        self.output_path: Path | None = None

        self._charts: ReportCharts | None = None

        logger.info(

            "ReportGenerator initialized for user %s",

            user_id,

        )

    # =====================================================
    # FILE HELPERS
    # =====================================================

    def _build_filename(
        self,
    ) -> str:
        """
        Create a unique filename.
        """

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        return (

            f"Finacle_Report_"

            f"{self.user_id}_"

            f"{timestamp}.pdf"

        )

    # -----------------------------------------------------

    def _build_output_path(
        self,
    ) -> Path:
        """
        Build the complete output path.
        """

        return (

            self.output_directory

            / self._build_filename()

        )

    # -----------------------------------------------------

    @staticmethod
    def _validate_report(
        report: dict[str, Any],
    ) -> None:
        """
        Validate report data before
        generating the PDF.
        """

        if not report:

            raise ValueError(
                "Report data is empty."
            )

        required = [

            "summary",

            "cashflow",

            "prediction",

            "allocation",

            "financial_score",

            "transactions",

        ]

        missing = [

            key

            for key in required

            if key not in report

        ]

        if missing:

            raise ValueError(

                "Missing report sections: "

                + ", ".join(missing)

            )

    # =====================================================
    # PREPARE REPORT
    # =====================================================

    def _prepare_report(
        self,
    ) -> None:
        """
        Build the complete report dataset.
        """

        logger.info(
            "Preparing report data..."
        )

        service = ReportDataService(
            self.user_id
        )

        self.report_data = (
            service.build_report()
        )

        self._validate_report(
            self.report_data
        )

        logger.info(
            "Report data prepared successfully."
        )

    # -----------------------------------------------------

    def _prepare_charts(
        self,
    ) -> None:
        """
        Generate all report charts.
        """

        logger.info(
            "Generating report charts..."
        )

        self._charts = ReportCharts()

        self.chart_paths = (
            self._charts.generate_all(
                self.report_data
            )
        )

        logger.info(

            "%d chart(s) generated.",

            len(self.chart_paths),

        )

    # -----------------------------------------------------

    def _create_canvas(
        self,
    ) -> canvas.Canvas:
        """
        Create the ReportLab canvas.
        """

        self.output_path = (
            self._build_output_path()
        )

        logger.info(
            "Creating PDF canvas..."
        )

        pdf = canvas.Canvas(
            str(self.output_path)
        )

        pdf.setTitle(
            "Finacle Financial Report"
        )

        pdf.setAuthor(
            "Finacle"
        )

        pdf.setSubject(
            "Personal Finance Report"
        )

        return pdf

    # -----------------------------------------------------

    def _build_pages(
        self,
        pdf: canvas.Canvas,
    ) -> ReportPages:
        """
        Create the page renderer.
        """

        logger.info(
            "Initializing ReportPages..."
        )

        return ReportPages(

            canvas=pdf,

            report_data=self.report_data,

            chart_paths=self.chart_paths,

        )
    # =====================================================
    # GENERATE PDF
    # =====================================================

    def generate(
        self,
    ) -> Path:
        """
        Generate the complete PDF report.

        Returns
        -------
        Path
            Path to the generated PDF.
        """

        logger.info(

            "Starting PDF generation for user %s",

            self.user_id,

        )

        try:

            # ---------------------------------------------
            # STEP 1 : Build report data
            # ---------------------------------------------

            self._prepare_report()

            # ---------------------------------------------
            # STEP 2 : Generate charts
            # ---------------------------------------------

            self._prepare_charts()

            # ---------------------------------------------
            # STEP 3 : Create PDF canvas
            # ---------------------------------------------

            pdf = self._create_canvas()

            # ---------------------------------------------
            # STEP 4 : Render pages
            # ---------------------------------------------

            pages = self._build_pages(
                pdf
            )

            pages.render()

            # ---------------------------------------------
            # STEP 5 : Save PDF
            # ---------------------------------------------

            pdf.save()

            logger.info(

                "PDF generated successfully."

            )

            return self.output_path

        except Exception as exc:

            logger.exception(
                "PDF generation failed."
            )

            raise RuntimeError(

                f"PDF generation failed: {exc}"

            ) from exc

        finally:

            if self._charts is not None:

                try:

                    self._charts.cleanup()

                    logger.info(
                        "Temporary charts removed."
                    )

                except Exception:

                    logger.exception(

                        "Unable to clean temporary charts."

                    )
        # -----------------------------------------------------
    # STRING HELPER
    # -----------------------------------------------------             
    def generate_as_string(
        self,
    ) -> str:
        """
        Generate the report and return
        the PDF path as a string.
        """

        return str(
            self.generate()
        )

    # -----------------------------------------------------
    # EXISTS
    # -----------------------------------------------------

    def exists(
        self,
    ) -> bool:
        """
        Check whether the generated
        PDF exists.
        """

        return (

            self.output_path is not None

            and

            self.output_path.exists()

        )

    # =====================================================
    # PUBLIC HELPERS
    # =====================================================

    def get_output_path(
        self,
    ) -> Path | None:
        """
        Return generated PDF path.
        """

        return self.output_path

    # -----------------------------------------------------

    def get_chart_paths(
        self,
    ) -> dict[str, str]:
        """
        Return generated chart paths.
        """

        return dict(
            self.chart_paths
        )

    # -----------------------------------------------------

    def get_report_data(
        self,
    ) -> dict[str, Any]:
        """
        Return prepared report data.
        """

        return dict(
            self.report_data
        )

    # -----------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset the generator so the
        instance can be reused.
        """

        self.report_data.clear()

        self.chart_paths.clear()

        self.output_path = None

        self._charts = None

        logger.info(
            "ReportGenerator reset completed."
        )
                    