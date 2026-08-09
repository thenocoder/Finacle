"""
=========================================================
Finacle PDF Report Pages
=========================================================

Professional PDF rendering engine.

Responsible ONLY for rendering.

No calculations are performed here.
"""

from __future__ import annotations

import logging

from datetime import datetime

from pathlib import Path

from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

from services.report_styles import styles


logger = logging.getLogger(__name__)


class ReportPages:
    """
    Responsible for rendering
    the complete PDF report.

    Uses prepared data only.
    """

    PAGE_WIDTH = 595.27
    PAGE_HEIGHT = 841.89

    LEFT_MARGIN = 42
    RIGHT_MARGIN = 42

    TOP_MARGIN = 42
    BOTTOM_MARGIN = 36

    HEADER_HEIGHT = 58
    FOOTER_HEIGHT = 28

    CONTENT_WIDTH = (
        PAGE_WIDTH
        - LEFT_MARGIN
        - RIGHT_MARGIN
    )

    CONTENT_HEIGHT = (
        PAGE_HEIGHT
        - TOP_MARGIN
        - BOTTOM_MARGIN
        - HEADER_HEIGHT
        - FOOTER_HEIGHT
    )

    CARD_RADIUS = 10

    SECTION_GAP = 18

    ELEMENT_GAP = 12

    CHART_PADDING = 10

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(
        self,
        canvas,
        report_data: dict[str, Any],
        chart_paths: dict[str, str],
    ) -> None:

        self.canvas = canvas

        self.data = report_data or {}

        self.chart_paths = chart_paths or {}

        self.styles = styles

        self.cursor_y = (
            self.PAGE_HEIGHT
            - self.TOP_MARGIN
            - self.HEADER_HEIGHT
        )

        logger.info(
            "ReportPages initialized."
        )

    # =====================================================
    # CURSOR HELPERS
    # =====================================================

    def reset_cursor(
        self,
    ) -> None:

        self.cursor_y = (
            self.PAGE_HEIGHT
            - self.TOP_MARGIN
            - self.HEADER_HEIGHT
        )

    # -----------------------------------------------------

    def move_cursor(
        self,
        amount: float,
    ) -> float:

        self.cursor_y -= amount

        return self.cursor_y

    # =====================================================
    # IMAGE HELPERS
    # =====================================================

    @staticmethod
    def _image_size(
        path: str,
    ):

        try:

            image = ImageReader(
                path
            )

            return image.getSize()

        except Exception:

            return None

    # -----------------------------------------------------

    @staticmethod
    def _wrap(
        text: str,
        length: int = 30,
    ) -> str:
        """
        Wrap long text.
        """

        if not text:

            return ""

        if len(text) <= length:

            return text

        return text[:length] + "..."

    # -----------------------------------------------------

    def _draw_chart(
        self,
        path: str,
        x: float,
        y: float,
        width: float,
        max_height: float,
    ) -> None:

        if (

            not path

            or

            not Path(path).exists()

        ):

            return

        size = self._image_size(
            path
        )

        if size is None:

            return

        original_width, original_height = size

        scale = min(

            width / original_width,

            max_height / original_height,

        )

        draw_width = original_width * scale

        draw_height = original_height * scale

        self.canvas.drawImage(

            path,

            x,

            y + (

                max_height

                - draw_height

            ) / 2,

            width=draw_width,

            height=draw_height,

            preserveAspectRatio=True,

            mask="auto",

        )

    # =====================================================
    # HEADER
    # =====================================================

    def _draw_header(
        self,
        title: str,
    ) -> None:

        c = self.canvas

        c.setFillColor(
            self.styles.PRIMARY
        )

        c.rect(

            0,

            self.PAGE_HEIGHT
            - self.HEADER_HEIGHT,

            self.PAGE_WIDTH,

            self.HEADER_HEIGHT,

            stroke=0,

            fill=1,

        )

        c.setFillColor(
            colors.white
        )

        c.setFont(
            self.styles.bold,
            20,
        )

        c.drawString(

            self.LEFT_MARGIN,

            self.PAGE_HEIGHT - 38,

            title,

        )

        generated = str(

            self.data.get(

                "generated_at",

                datetime.now().strftime(
                    "%d %b %Y %H:%M"
                ),

            )

        )

        c.setFont(
            self.styles.bold,
            10,
        )

        c.drawRightString(

            self.PAGE_WIDTH
            - self.RIGHT_MARGIN,

            self.PAGE_HEIGHT - 38,

            generated,

        )

    # =====================================================
    # FOOTER
    # =====================================================

    def _draw_footer(
        self,
        page_number: int,
    ) -> None:

        c = self.canvas

        c.setStrokeColor(
            colors.lightgrey
        )

        c.line(

            self.LEFT_MARGIN,

            self.FOOTER_HEIGHT,

            self.PAGE_WIDTH
            - self.RIGHT_MARGIN,

            self.FOOTER_HEIGHT,

        )

        c.setFillColor(
            colors.grey
        )

        c.setFont(
            self.styles.bold,
            9,
        )

        c.drawString(

            self.LEFT_MARGIN,

            16,

            "Generated by Finacle",

        )

        c.drawRightString(

            self.PAGE_WIDTH
            - self.RIGHT_MARGIN,

            16,

            f"Page {page_number}",

        )

    # =====================================================
    # SECTION TITLE
    # =====================================================

    def _draw_section_title(
        self,
        title: str,
    ) -> None:

        c = self.canvas

        self.move_cursor(12)

        c.setFillColor(
            self.styles.PRIMARY
        )

        c.setFont(
            self.styles.bold,
            16,
        )

        c.drawString(

            self.LEFT_MARGIN,

            self.cursor_y,

            title,

        )

        self.move_cursor(8)

        c.setStrokeColor(
            colors.lightgrey
        )

        c.setLineWidth(0.7)

        c.line(

            self.LEFT_MARGIN,

            self.cursor_y,

            self.PAGE_WIDTH
            - self.RIGHT_MARGIN,

            self.cursor_y,

        )

        self.move_cursor(18)

    # =====================================================
    # INFO CARD
    # =====================================================

    def _draw_info_card(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        title: str,
        value: str,
        accent_color=None,
    ) -> None:

        c = self.canvas

        accent_color = (
            accent_color
            or self.styles.PRIMARY
        )

        c.setFillColor(
            colors.white
        )

        c.setStrokeColor(
            colors.HexColor("#D6D6D6")
        )

        c.roundRect(

            x,

            y,

            width,

            height,

            self.CARD_RADIUS,

            stroke=1,

            fill=1,

        )

        c.setFillColor(
            accent_color
        )

        c.rect(

            x,

            y + height - 5,

            width,

            5,

            stroke=0,

            fill=1,

        )

        c.setFillColor(
            colors.grey
        )

        c.setFont(
            self.styles.bold,
            10,
        )

        c.drawString(

            x + 12,

            y + height - 22,

            title,

        )

        c.setFillColor(
            colors.black
        )

        c.setFont(
            self.styles.bold,
            16,
        )

        c.drawString(

            x + 12,

            y + 16,

            str(value),

        )

    # =====================================================
    # PAGE 1
    # =====================================================
        # =====================================================
    # PAGE 1
    # =====================================================

    def page1_overview(
        self,
    ) -> None:
        """
        Render Executive Summary.
        """

        c = self.canvas

        self.reset_cursor()

        self._draw_header(
            "Executive Summary"
        )

        summary = self.data.get(
            "summary",
            {},
        )

        score = self.data.get(
            "financial_score",
            {},
        )

        insights = self.data.get(
            "insights",
            [],
        )

        user = self.data.get(
            "user",
            {},
        )

        # -------------------------------------------------
        # USER INFORMATION
        # -------------------------------------------------

        self._draw_section_title(
            "User Information"
        )

        c.setFont(
            self.styles.bold,
            11,
        )

        info_y = self.cursor_y

        c.drawString(
            self.LEFT_MARGIN,
            info_y,
            f"Name : {user.get('name', 'N/A')}",
        )

        c.drawString(
            self.LEFT_MARGIN,
            info_y - 18,
            f"Email : {user.get('email', 'N/A')}",
        )

        generated = self.data.get(
            "generated_at",
            "N/A",
        )

        c.drawString(
            self.LEFT_MARGIN,
            info_y - 36,
            f"Generated : {generated}",
        )

        self.move_cursor(72)

        # -------------------------------------------------
        # KPI CARDS
        # -------------------------------------------------

        self._draw_section_title(
            "Financial Summary"
        )

        card_width = 135
        card_height = 55
        gap = 12

        y = self.cursor_y - card_height

        cards = [

            (
                "Income",
                f"₹{summary.get('income',0):,.2f}",
                colors.green,
            ),

            (
                "Expense",
                f"₹{summary.get('expense',0):,.2f}",
                colors.red,
            ),

            (
                "Savings",
                f"₹{summary.get('savings',0):,.2f}",
                colors.blue,
            ),

            (
                "Saving Rate",
                f"{summary.get('saving_rate',0):.1f}%",
                colors.orange,
            ),

        ]

        for index, card in enumerate(cards):

            x = self.LEFT_MARGIN + index * (
                card_width + gap
            )

            self._draw_info_card(

                x,

                y,

                card_width,

                card_height,

                card[0],

                card[1],

                card[2],

            )

        self.move_cursor(
            card_height + 30
        )
        
        

        # -------------------------------------------------
        # FINANCIAL HEALTH
        # -------------------------------------------------

       

        # -------------------------------------------------
        # EXECUTIVE INSIGHTS
        # -------------------------------------------------

        self._draw_section_title(
            "Executive Insights"
        )

        c.setFont(
            self.styles.bold,
            10,
        )

        line_y = self.cursor_y

        if insights:

            for item in insights[:6]:

                if line_y < 80:
                    break

                text = self._wrap(
                    str(item),
                    78,
                )

                c.drawString(
                    self.LEFT_MARGIN,
                    line_y,
                    f"• {text}",
                )

                line_y -= 16
            else:
                c.drawString(
                                self.LEFT_MARGIN,
                                line_y,
                                "No financial insights available.",
                            )
             
    
            

        # -------------------------------------------------
        # REPORT CONCLUSION
        # -------------------------------------------------

        
        self._draw_footer(
            page_number=1,
        )
        self.canvas.showPage()

       

    # =====================================================
    # PAGE 2
    # =====================================================
        # =====================================================
    # PAGE 2
    # =====================================================

    def page2_analytics(
        self,
    ) -> None:
        """
        Render the Financial Analytics page.
        """

        c = self.canvas

        self.reset_cursor()

        self._draw_header(
            "Financial Analytics"
        )

        cashflow = self.data.get(
            "cashflow",
            {},
        )

        monthly_statistics = self.data.get(
            "monthly_statistics",
            {},
        )

        spending = self.data.get(
            "spending_behaviour",
            {},
        )

        self._draw_section_title(
            "Cash Flow Overview"
        )

        card_width = 135
        card_height = 55
        gap = 12

        y = self.cursor_y - card_height

        cards = [

            (
                "Cash Flow",
                f"₹{cashflow.get('cashflow',0):,.2f}",
                colors.blue,
            ),

            (
                "Saving Rate",
                f"{cashflow.get('saving_rate',0):.1f}%",
                colors.green,
            ),

            (
                "Status",
                cashflow.get(
                    "status",
                    "N/A",
                ),
                colors.orange,
            ),

            (
                "Top Category",
                spending.get(
                    "primary_category",
                    "N/A",
                ),
                colors.purple,
            ),

        ]

        for index, card in enumerate(cards):

            x = self.LEFT_MARGIN + index * (
                card_width + gap
            )

            self._draw_info_card(

                x,

                y,

                card_width,

                card_height,

                card[0],

                str(card[1]),

                card[2],

            )

        self.move_cursor(
            card_height + 30
        )

        # -------------------------------------------------
        # MONTHLY STATISTICS
        # -------------------------------------------------
                # -------------------------------------------------
        # MONTHLY STATISTICS
        # -------------------------------------------------

        self._draw_section_title(
            "Monthly Statistics"
        )

        c.setFont(
            self.styles.bold,
            11,
        )

        stats = [

            (
                "Average Income",
                monthly_statistics.get(
                    "average_income",
                    0,
                ),
            ),

            (
                "Average Expense",
                monthly_statistics.get(
                    "average_expense",
                    0,
                ),
            ),

            (
                "Average Cash Flow",
                monthly_statistics.get(
                    "average_cashflow",
                    0,
                ),
            ),

            (
                "Highest Income",
                monthly_statistics.get(
                    "highest_income",
                    0,
                ),
            ),

            (
                "Highest Expense",
                monthly_statistics.get(
                    "highest_expense",
                    0,
                ),
            ),

        ]

        label_x = self.LEFT_MARGIN
        value_x = self.PAGE_WIDTH - self.RIGHT_MARGIN

        row_height = 18

        y = self.cursor_y

        for label, value in stats:

            c.drawString(
                label_x,
                y,
                label,
            )

            c.drawRightString(
                value_x,
                y,
                f"₹{value:,.2f}",
            )

            y -= row_height

        self.cursor_y = y - 12

        # -------------------------------------------------
        # SPENDING BEHAVIOUR
        # -------------------------------------------------
                # -------------------------------------------------
        # SPENDING BEHAVIOUR
        # -------------------------------------------------

        self._draw_section_title(
            "Spending Behaviour"
        )

        c.setFont(
            self.styles.bold,
            11,
        )

        behaviour_rows = [

            (
                "Primary Category",
                spending.get(
                    "primary_category",
                    "N/A",
                ),
            ),

            (
                "Largest Share",
                f"{spending.get('largest_percentage', 0):.1f}%",
            ),

            (
                "Expense Ratio",
                f"{spending.get('expense_ratio', 0):.1f}%",
            ),

            (
                "Behaviour",
                spending.get(
                    "behaviour",
                    "N/A",
                ),
            ),

        ]

        label_x = self.LEFT_MARGIN
        value_x = self.PAGE_WIDTH - self.RIGHT_MARGIN

        row_height = 18

        y = self.cursor_y

        for label, value in behaviour_rows:

            c.drawString(
                label_x,
                y,
                label,
            )

            c.drawRightString(
                value_x,
                y,
                str(value),
            )

            y -= row_height

        self.cursor_y = y - 15

        # -------------------------------------------------
        # FINANCIAL CHARTS
        # -------------------------------------------------
                # -------------------------------------------------
        # FINANCIAL CHARTS
        # -------------------------------------------------

        self._draw_section_title(
            "Financial Charts"
        )

        left_chart = self.chart_paths.get(
            "cashflow_chart"
        )

        right_chart = self.chart_paths.get(
            "expense_distribution_chart"
        )

        chart_width = 260
        chart_height = 190

        chart_y = 70

        left_x = self.LEFT_MARGIN

        right_x = (
            self.PAGE_WIDTH
            - self.RIGHT_MARGIN
            - chart_width
        )

        self._draw_chart(

            left_chart,

            left_x,

            chart_y,

            chart_width,

            chart_height,

        )

        self._draw_chart(

            right_chart,

            right_x,

            chart_y,

            chart_width,

            chart_height,

        )

        # -------------------------------------------------
        # FOOTER
        # -------------------------------------------------

        self._draw_footer(
            page_number=2,
        )

        self.canvas.showPage()
            # =====================================================
    # PAGE 3
    # =====================================================

    def page3_ai(
        self,
    ) -> None:
        """
        Render AI Financial Intelligence page.
        """

        c = self.canvas

        self.reset_cursor()

        self._draw_header(
            "AI Financial Intelligence"
        )

        prediction = self.data.get(
            "prediction",
            {},
        )

        allocation = self.data.get(
            "allocation",
            {},
        )

        financial_dna = self.data.get(
            "financial_dna",
            {},
        )

        recommendations = self.data.get(
            "recommendations",
            [],
        )

        goals = self.data.get(
            "financial_goals",
            [],
        )

        # -------------------------------------------------
        # EXPENSE PREDICTION
        # -------------------------------------------------

        self._draw_section_title(
            "Expense Prediction"
        )

        card_width = 135
        card_height = 55
        gap = 12

        y = self.cursor_y - card_height

        prediction_cards = [

            (
                "Predicted Expense",
                f"₹{prediction.get('predicted_expense', 0):,.2f}",
                colors.red,
            ),

            (
                "Expected Savings",
                f"₹{prediction.get('expected_savings', 0):,.2f}",
                colors.green,
            ),

            (
                "Confidence",
                f"{prediction.get('confidence', 0):.1f}%",
                colors.blue,
            ),

        ]

        for index, card in enumerate(
            prediction_cards
        ):

            x = self.LEFT_MARGIN + index * (
                card_width + gap
            )

            self._draw_info_card(

                x,

                y,

                card_width,

                card_height,

                card[0],

                card[1],

                card[2],

            )

        self.move_cursor(
            card_height + 30
        )

        c.setFont(
            self.styles.bold,
            11,
        )

        c.setFillColor(
            self.styles.PRIMARY
        )

        c.drawString(

            self.LEFT_MARGIN,

            self.cursor_y,

            "Expense Trend",

        )

        c.setFillColor(
            colors.black
        )

        c.drawString(

            self.LEFT_MARGIN + 120,

            self.cursor_y,

            str(
                prediction.get(
                    "trend",
                    "N/A",
                )
            ),

        )

        self.move_cursor(
            30
        )

        # -------------------------------------------------
        # SMART ALLOCATION
        # -------------------------------------------------
                # -------------------------------------------------
        # SMART ALLOCATION
        # -------------------------------------------------

        self._draw_section_title(
            "Smart Allocation"
        )

        allocation_chart = self.chart_paths.get(
            "allocation_chart"
        )

        chart_width = 210
        chart_height = 165

        chart_x = self.LEFT_MARGIN
        chart_y = self.cursor_y - chart_height

        self._draw_chart(

            allocation_chart,

            chart_x,

            chart_y,

            chart_width,

            chart_height,

        )

        table_x = 290

        table_y = self.cursor_y

        c.setFont(
            self.styles.bold,
            11,
        )

        c.drawString(
            table_x,
            table_y,
            "Recommended Allocation",
        )

        table_y -= 20

        c.setFont(
            self.styles.bold,
            10,
        )

        allocations = allocation.get(
            "allocations",
            [],
        )

        if allocations:

            for item in allocations:

                if table_y < chart_y + 12:
                    break

                name = str(
                    item.get(
                        "name",
                        "",
                    )
                )

                amount = float(
                    item.get(
                        "amount",
                        0,
                    )
                )

                c.drawString(
                    table_x,
                    table_y,
                    self._wrap(
                        name,
                        22,
                    ),
                )

                c.drawRightString(
                    self.PAGE_WIDTH
                    - self.RIGHT_MARGIN,
                    table_y,
                    f"₹{amount:,.2f}",
                )

                table_y -= 18

        else:

            c.drawString(
                table_x,
                table_y,
                "No allocation available.",
            )

        self.cursor_y = chart_y - 22

        # -------------------------------------------------
        # FINANCIAL DNA
        # -------------------------------------------------
                # -------------------------------------------------
        # FINANCIAL DNA
        # -------------------------------------------------

        self._draw_section_title(
            "Financial DNA"
        )

        c.setFont(
            self.styles.bold,
            11,
        )

        dna_items = [

            (
                "Risk Profile",
                financial_dna.get(
                    "risk_profile",
                    "N/A",
                ),
            ),

            (
                "Financial Goal",
                financial_dna.get(
                    "goal",
                    "N/A",
                ),
            ),

            (
                "Investment Horizon",
                financial_dna.get(
                    "investment_horizon",
                    "N/A",
                ),
            ),

            (
                "Spender Type",
                financial_dna.get(
                    "spender_type",
                    "N/A",
                ),
            ),

            (
                "Investor Type",
                financial_dna.get(
                    "investor_type",
                    "N/A",
                ),
            ),

        ]

        label_x = self.LEFT_MARGIN

        value_x = (
            self.PAGE_WIDTH
            - self.RIGHT_MARGIN
        )

        row_height = 18

        dna_y = self.cursor_y

        for label, value in dna_items:

            if dna_y < 170:
                break

            c.drawString(

                label_x,

                dna_y,

                label,

            )

            c.drawRightString(

                value_x,

                dna_y,

                str(value),

            )

            dna_y -= row_height

        self.cursor_y = dna_y - 12

        # -------------------------------------------------
        # RECOMMENDATIONS
        # -------------------------------------------------
                # -------------------------------------------------
        # RECOMMENDATIONS
        # -------------------------------------------------

        self._draw_section_title(
            "Recommendations"
        )

        c.setFont(
            self.styles.bold,
            10,
        )

        recommendation_y = self.cursor_y

        if recommendations:

            for recommendation in recommendations[:5]:

                if recommendation_y < 110:
                    break

                c.drawString(

                    self.LEFT_MARGIN,

                    recommendation_y,

                    f"• {self._wrap(str(recommendation), 75)}",

                )

                recommendation_y -= 18

        else:

            c.drawString(

                self.LEFT_MARGIN,

                recommendation_y,

                "No recommendations available.",

            )

            recommendation_y -= 18

        self.cursor_y = recommendation_y - 12

        # -------------------------------------------------
        # FINANCIAL GOALS
        # -------------------------------------------------

        self._draw_section_title(
            "Financial Goals"
        )

        c.setFont(
            self.styles.bold,
            10,
        )

        goal_y = self.cursor_y

        if goals:

            for goal in goals[:4]:

                if goal_y < 55:
                    break

                title = str(

                    goal.get(

                        "title",

                        "Goal",

                    )

                )

                progress = float(

                    goal.get(

                        "progress",

                        0,

                    )

                )

                c.drawString(

                    self.LEFT_MARGIN,

                    goal_y,

                    self._wrap(

                        title,

                        42,

                    ),

                )

                c.drawRightString(

                    self.PAGE_WIDTH
                    - self.RIGHT_MARGIN,

                    goal_y,

                    f"{progress:.0f}%",

                )

                goal_y -= 18

        else:

            c.drawString(

                self.LEFT_MARGIN,

                goal_y,

                "No financial goals available.",

            )

            goal_y -= 18

        self._draw_footer(
            page_number=3,
        )

        self.canvas.showPage()
            # =====================================================
    # PAGE 4
    # =====================================================

    def page4_transactions(
        self,
    ) -> None:
        """
        Render Transactions & Summary page.
        """

        c = self.canvas

        self.reset_cursor()

        self._draw_header(
            "Transactions & Summary"
        )

        transactions = self.data.get(
            "transactions",
            [],
        )

        largest = self.data.get(
            "largest_expenses",
            [],
        )

        # -------------------------------------------------
        # LARGEST EXPENSES
        # -------------------------------------------------

        self._draw_section_title(
            "Largest Expenses"
        )

        header_y = self.cursor_y

        c.setFont(
            self.styles.bold,
            10,
        )

        columns = [

            ("Title", self.LEFT_MARGIN),

            ("Category", 190),

            ("Date", 310),

            ("Method", 400),

            ("Amount", 545),

        ]

        for title, x in columns:

            if title == "Amount":

                c.drawRightString(
                    x,
                    header_y,
                    title,
                )

            else:

                c.drawString(
                    x,
                    header_y,
                    title,
                )

        y = header_y - 18

        c.setFont(
            self.styles.bold,
            9,
        )

        if largest:

            for item in largest[:8]:

                if y < 410:
                    break

                c.drawString(
                    self.LEFT_MARGIN,
                    y,
                    str(item.get("title", ""))[:28],
                )

                c.drawString(
                    190,
                    y,
                    str(item.get("category", ""))[:15],
                )

                c.drawString(
                    310,
                    y,
                    str(item.get("date", "")),
                )

                c.drawString(
                    400,
                    y,
                    str(item.get("payment_method", "")),
                )

                c.drawRightString(
                    545,
                    y,
                    f"₹{float(item.get('amount',0)):,.2f}",
                )

                y -= 18

        else:

            c.drawString(
                self.LEFT_MARGIN,
                y,
                "No expense data available.",
            )

            y -= 18

        self.cursor_y = y - 20

        # -------------------------------------------------
        # RECENT TRANSACTIONS
        # -------------------------------------------------

        self._draw_section_title(
            "Recent Transactions"
        )

        header_y = self.cursor_y

        c.setFont(
            self.styles.bold,
            10,
        )

        columns = [

            ("Date", self.LEFT_MARGIN),

            ("Category", 120),

            ("Type", 240),

            ("Amount", 340),

            ("Description", 430),

        ]

        for title, x in columns:

            c.drawString(
                x,
                header_y,
                title,
            )

        y = header_y - 18

        c.setFont(
            self.styles.bold,
            8,
        )

        if transactions:

            for txn in transactions[:15]:

                if y < 80:
                    break

                c.drawString(
                    self.LEFT_MARGIN,
                    y,
                    str(txn.get("date", "")),
                )

                c.drawString(
                    120,
                    y,
                    str(txn.get("category", ""))[:15],
                )

                c.drawString(
                    240,
                    y,
                    str(txn.get("type", "")),
                )

                c.drawRightString(
                    395,
                    y,
                    f"₹{float(txn.get('amount',0)):,.2f}",
                )

                c.drawString(
                    430,
                    y,
                    str(txn.get("title", ""))[:20],
                )

                y -= 16

        else:

            c.drawString(
                self.LEFT_MARGIN,
                y,
                "No transaction history available.",
            )

        self._draw_footer(
            page_number=4,
        )

        self.canvas.showPage()
            # =====================================================
    # PUBLIC RENDER
    # =====================================================

    def render(
        self,
    ) -> None:
        """
        Render the complete Finacle report.

        This method renders every page
        in the correct order.

        It DOES NOT save the PDF.
        ReportGenerator is responsible
        for calling canvas.save().
        """

        logger.info(
            "Rendering PDF pages..."
        )

        self.page1_overview()

        self.page2_analytics()

        self.page3_ai()

        self.page4_transactions()

        logger.info(
            "All report pages rendered successfully."
        )