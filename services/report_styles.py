"""
=========================================================
Finacle PDF Report Styles
=========================================================

Central styling module for the Finacle PDF Reporting Engine.

Responsibilities
----------------
✓ Theme Colors
✓ Font Registration
✓ Paragraph Styles
✓ Table Styles
✓ Shared UI Constants

Contains no business logic.
"""

from __future__ import annotations

import logging

from copy import deepcopy
from pathlib import Path
from xml.dom.domreg import registered

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT,
    TA_RIGHT,
    TA_JUSTIFY,
)
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# PAGE DIMENSIONS
# ==========================================================

PAGE_WIDTH = 8.27 * inch
PAGE_HEIGHT = 11.69 * inch

PAGE_MARGIN_LEFT = 0.55 * inch
PAGE_MARGIN_RIGHT = 0.55 * inch
PAGE_MARGIN_TOP = 0.60 * inch
PAGE_MARGIN_BOTTOM = 0.55 * inch

CONTENT_WIDTH = (
    PAGE_WIDTH
    - PAGE_MARGIN_LEFT
    - PAGE_MARGIN_RIGHT
)

# ==========================================================
# COLOR PALETTE
# ==========================================================

PRIMARY = HexColor("#1E3A8A")
SECONDARY = HexColor("#2563EB")

SUCCESS = HexColor("#16A34A")
WARNING = HexColor("#F59E0B")
DANGER = HexColor("#DC2626")
INFO = HexColor("#0EA5E9")

BACKGROUND = HexColor("#F8FAFC")
CARD_BACKGROUND = colors.white

LIGHT_PRIMARY = HexColor("#DBEAFE")
LIGHT_SUCCESS = HexColor("#DCFCE7")
LIGHT_WARNING = HexColor("#FEF3C7")
LIGHT_DANGER = HexColor("#FEE2E2")

TEXT = HexColor("#111827")
TEXT_LIGHT = HexColor("#6B7280")
MUTED = HexColor("#94A3B8")

BORDER = HexColor("#E5E7EB")

# ==========================================================
# CHART PALETTE
# ==========================================================

CHART_COLORS = [

    HexColor("#2563EB"),
    HexColor("#16A34A"),
    HexColor("#F59E0B"),
    HexColor("#DC2626"),
    HexColor("#7C3AED"),
    HexColor("#EC4899"),
    HexColor("#0EA5E9"),
    HexColor("#14B8A6"),

]

# ==========================================================
# FONT REGISTRATION
# ==========================================================

def register_fonts() -> None:
    """
    Register custom fonts if available.
    Falls back to self.styles.bold.
    """

    try:

        font_dir = Path(__file__).resolve().parent / "fonts"

        regular = font_dir / "DejaVuSans.ttf"
        bold = font_dir / "DejaVuSans-Bold.ttf"

        if regular.exists():

            pdfmetrics.registerFont(
                TTFont(
                    "DejaVu",
                    str(regular)
                )
            )

            logger.info("Registered DejaVu font.")

        if bold.exists():

            pdfmetrics.registerFont(
                TTFont(
                    "DejaVu-Bold",
                    str(bold)
                )
            )

            logger.info("Registered DejaVu-Bold font.")

    except Exception:

        logger.exception(
            "Unable to register custom fonts. Falling back to self.styles.bold."
        )

# ==========================================================
# REPORT STYLES
# ==========================================================

class ReportStyles:
    """
    Central style manager for the PDF reporting engine.
    """

    def __init__(self) -> None:

        register_fonts()

        registered = pdfmetrics.getRegisteredFontNames()
       

        self.font = (
            "DejaVu"
            if "DejaVu" in registered
            else self.styles.bold
        )

        self.bold = (
            "DejaVu-Bold"
            if "DejaVu-Bold" in registered
            else self.styles.bold
        )
        print("Using font:", self.font)
        print("Using bold:", self.bold)


        self.styles = getSampleStyleSheet()

        self.chart_palette = deepcopy(
            CHART_COLORS
        )

        # Theme Colors

        self.PRIMARY = PRIMARY
        self.SECONDARY = SECONDARY

        self.SUCCESS = SUCCESS
        self.WARNING = WARNING
        self.DANGER = DANGER
        self.INFO = INFO

        self.BACKGROUND = BACKGROUND
        self.CARD_BACKGROUND = CARD_BACKGROUND

        self.BORDER = BORDER

        self.TEXT = TEXT
        self.TEXT_LIGHT = TEXT_LIGHT
        self.MUTED = MUTED

        self.LIGHT_PRIMARY = LIGHT_PRIMARY
        self.LIGHT_SUCCESS = LIGHT_SUCCESS
        self.LIGHT_WARNING = LIGHT_WARNING
        self.LIGHT_DANGER = LIGHT_DANGER

        self.CHART_COLORS = deepcopy(
            CHART_COLORS
        )

        self._build_styles()

        logger.info(
            "ReportStyles initialized successfully."
        )
            # ==========================================================
    # BUILD STYLES
    # ==========================================================

    def _build_styles(self) -> None:
        """
        Build all paragraph and table styles used by the
        Finacle PDF Reporting Engine.
        """

        base = self.styles["BodyText"]

        base.fontName = self.font
        base.fontSize = 10
        base.leading = 15
        base.textColor = self.TEXT
        base.alignment = TA_LEFT

        self.body = base

        # ------------------------------------------------------
        # Report Title
        # ------------------------------------------------------

        self.title = ParagraphStyle(
            "ReportTitle",
            parent=base,
            fontName=self.bold,
            fontSize=24,
            leading=28,
            alignment=TA_CENTER,
            textColor=self.PRIMARY,
            spaceAfter=18,
        )

        # ------------------------------------------------------
        # Main Heading
        # ------------------------------------------------------

        self.heading = ParagraphStyle(
            "Heading",
            parent=base,
            fontName=self.bold,
            fontSize=16,
            leading=20,
            textColor=self.PRIMARY,
            spaceBefore=8,
            spaceAfter=8,
        )

        # ------------------------------------------------------
        # Sub Heading
        # ------------------------------------------------------

        self.sub_heading = ParagraphStyle(
            "SubHeading",
            parent=base,
            fontName=self.bold,
            fontSize=13,
            leading=16,
            textColor=self.TEXT,
            spaceBefore=6,
            spaceAfter=5,
        )

        # ------------------------------------------------------
        # Caption
        # ------------------------------------------------------

        self.caption = ParagraphStyle(
            "Caption",
            parent=base,
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            textColor=self.TEXT_LIGHT,
        )

        # ------------------------------------------------------
        # Paragraph
        # ------------------------------------------------------

        self.paragraph = ParagraphStyle(
            "Paragraph",
            parent=base,
            fontSize=10,
            leading=16,
            alignment=TA_JUSTIFY,
            textColor=self.TEXT,
        )

        # ------------------------------------------------------
        # KPI
        # ------------------------------------------------------

        self.kpi = ParagraphStyle(
            "KPI",
            parent=base,
            fontName=self.bold,
            fontSize=20,
            leading=22,
            alignment=TA_CENTER,
            textColor=self.PRIMARY,
        )

        # ------------------------------------------------------
        # Table Header
        # ------------------------------------------------------

        self.table_header = ParagraphStyle(
            "TableHeader",
            parent=base,
            fontName=self.bold,
            fontSize=10,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.white,
        )

        # ------------------------------------------------------
        # Table Cell
        # ------------------------------------------------------

        self.table_cell = ParagraphStyle(
            "TableCell",
            parent=base,
            fontName=self.font,
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            textColor=self.TEXT,
        )

        # ------------------------------------------------------
        # Footer
        # ------------------------------------------------------

        self.footer = ParagraphStyle(
            "Footer",
            parent=base,
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            textColor=self.TEXT_LIGHT,
        )

        # ------------------------------------------------------
        # Table Style
        # ------------------------------------------------------

        self.table_style = TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), self.PRIMARY),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), self.bold),

            ("FONTSIZE", (0, 0), (-1, 0), 10),

            ("TOPPADDING", (0, 0), (-1, 0), 8),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("BACKGROUND", (0, 1), (-1, -1), colors.white),

            ("TEXTCOLOR", (0, 1), (-1, -1), self.TEXT),

            ("FONTNAME", (0, 1), (-1, -1), self.font),

            ("FONTSIZE", (0, 1), (-1, -1), 9),

            ("GRID", (0, 0), (-1, -1), 0.3, self.BORDER),

            ("BOX", (0, 0), (-1, -1), 0.5, self.BORDER),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("LEFTPADDING", (0, 0), (-1, -1), 6),

            ("RIGHTPADDING", (0, 0), (-1, -1), 6),

            ("TOPPADDING", (0, 1), (-1, -1), 6),

            ("BOTTOMPADDING", (0, 1), (-1, -1), 6),

        ])

        logger.info(
            "Report styles built successfully."
        )
            # ==========================================================
    # Helper Methods
    # ==========================================================

    def score_color(self, score: float) -> HexColor:
        """
        Return the appropriate color for a financial score.

        Parameters
        ----------
        score : float
            Financial score (0-100).

        Returns
        -------
        HexColor
        """

        try:
            score = float(score)
        except (TypeError, ValueError):
            logger.warning(
                "Invalid score '%s'. Using danger color.",
                score
            )
            return self.DANGER

        if score >= 90:
            return self.SUCCESS

        if score >= 75:
            return HexColor("#22C55E")

        if score >= 60:
            return self.WARNING

        return self.DANGER

    # ------------------------------------------------------

    def currency_color(self, value: float):
        """
        Return a color representing the value.

        Positive  -> Green
        Negative  -> Red
        Zero      -> Default text
        """

        try:
            value = float(value)
        except (TypeError, ValueError):
            logger.warning(
                "Invalid currency value '%s'.",
                value
            )
            return self.TEXT

        if value > 0:
            return self.SUCCESS

        if value < 0:
            return self.DANGER

        return self.TEXT

    # ------------------------------------------------------

    def percentage_color(self, value: float):
        """
        Return a color for percentage values.
        """

        try:
            value = float(value)
        except (TypeError, ValueError):
            logger.warning(
                "Invalid percentage '%s'.",
                value
            )
            return self.TEXT

        if value >= 75:
            return self.SUCCESS

        if value >= 50:
            return self.WARNING

        return self.DANGER


# ==========================================================
# Global Style Instance
# ==========================================================

try:

    styles = ReportStyles()

    logger.info(
        "Global ReportStyles instance created successfully."
    )

except Exception:

    logger.exception(
        "Failed to initialize ReportStyles."
    )

    raise
