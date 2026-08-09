"""
=========================================================
Finacle PDF Report Charts
=========================================================

Professional chart rendering engine used by the
Finacle PDF Reporting Module.

This module ONLY generates charts.

No calculations are performed here.

Compatible with:
    • report_data.py
    • report_generator.py
    • report_pages.py
"""

from __future__ import annotations

import logging
import tempfile
import textwrap
import uuid

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


logger = logging.getLogger(__name__)

# ==========================================================
# CHART CONFIGURATION
# ==========================================================

DEFAULT_DPI = 350

DEFAULT_WIDTH = 9.5
DEFAULT_HEIGHT = 5.8

PIE_WIDTH = 8.4
PIE_HEIGHT = 7.0

GRID_ALPHA = 0.25

TITLE_SIZE = 16
LABEL_SIZE = 11
TICK_SIZE = 10
LEGEND_SIZE = 10

COLOR_INCOME = "#2E8B57"
COLOR_EXPENSE = "#DC3545"
COLOR_CASHFLOW = "#0D6EFD"

CHART_COLORS = [

    "#4E79A7",
    "#F28E2B",
    "#59A14F",
    "#E15759",
    "#76B7B2",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7",
    "#9C755F",
    "#BAB0AC",

]

BACKGROUND = "white"

# ==========================================================
# REPORT CHART ENGINE
# ==========================================================

class ReportCharts:
    """
    Professional chart rendering engine.

    Generates:

    • Cash Flow Chart
    • Monthly Trend Chart
    • Expense Distribution Chart
    • Smart Allocation Chart
    """

    def __init__(
        self,
    ) -> None:

        self.output_dir = (

            Path(
                tempfile.gettempdir()
            )

            / "finacle_report_charts"

        )

        self.output_dir.mkdir(

            parents=True,

            exist_ok=True,

        )

        plt.rcParams.update({

            "figure.dpi": DEFAULT_DPI,

            "figure.facecolor": BACKGROUND,

            "savefig.facecolor": BACKGROUND,

            "axes.facecolor": BACKGROUND,

            "font.family": "DejaVu Sans",

            "axes.titlesize": TITLE_SIZE,

            "axes.labelsize": LABEL_SIZE,

            "xtick.labelsize": TICK_SIZE,

            "ytick.labelsize": TICK_SIZE,

            "legend.fontsize": LEGEND_SIZE,

            "axes.grid": True,

            "grid.alpha": GRID_ALPHA,

            "grid.linestyle": "--",

            "axes.spines.top": False,

            "axes.spines.right": False,

            "axes.titleweight": "bold",

            "figure.autolayout": False,

        })

        logger.info(
            "ReportCharts initialized successfully."
        )

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    def _new_filename(
        self,
        prefix: str,
    ) -> Path:
        """
        Create a unique filename for a chart.
        """

        return (

            self.output_dir

            / f"{prefix}_{uuid.uuid4().hex}.png"

        )

    # -----------------------------------------------------

    def _create_figure(

        self,

        width: float = DEFAULT_WIDTH,

        height: float = DEFAULT_HEIGHT,

    ):

        fig, ax = plt.subplots(

            figsize=(width, height),

            constrained_layout=True,

        )

        return fig, ax

    # -----------------------------------------------------

    @staticmethod
    def _currency_formatter():

        return FuncFormatter(

            lambda value, _:

            f"₹{value:,.0f}"

        )

    # -----------------------------------------------------

    @staticmethod
    def _wrap(

        text: str,

        width: int = 14,

    ) -> str:

        if not text:

            return ""

        return "\n".join(

            textwrap.wrap(

                str(text),

                width=width,

            )

        )

    # -----------------------------------------------------

    def _style_axis(

        self,

        ax,

        title: str,

        ylabel: str = "",

    ) -> None:
        """
        Apply consistent styling to all charts.
        """

        ax.set_title(

            title,

            pad=18,

            fontweight="bold",

        )

        if ylabel:

            ax.set_ylabel(
                ylabel
            )

        ax.yaxis.set_major_formatter(

            self._currency_formatter()

        )

        ax.grid(

            axis="y",

            linestyle="--",

            linewidth=0.7,

            alpha=GRID_ALPHA,

        )

        ax.margins(

            x=0.03,

            y=0.08,

        )

    # -----------------------------------------------------

    def _save_chart(

        self,

        fig,

        filename: Path,

    ) -> str:
        """
        Save chart as a high-quality PNG.
        """

        fig.savefig(

            filename,

            dpi=DEFAULT_DPI,

            bbox_inches="tight",

            pad_inches=0.35,

        )

        plt.close(fig)

        logger.info(

            "Chart saved -> %s",

            filename,

        )

        return str(filename)

    # -----------------------------------------------------

    def _empty_chart(

        self,

        title: str = "No Data Available",

    ) -> str:
        """
        Generate placeholder chart.
        """

        fig, ax = self._create_figure()

        ax.axis("off")

        ax.text(

            0.5,

            0.5,

            title,

            ha="center",

            va="center",

            fontsize=20,

            fontweight="bold",

            color="#777777",

        )

        filename = self._new_filename(
            "empty"
        )

        return self._save_chart(

            fig,

            filename,

        )

    # -----------------------------------------------------

    @staticmethod
    def _autopct(
        values,
    ):
        """
        Hide labels below 4%.
        """

        total = sum(values)

        if total <= 0:

            return lambda pct: ""

        def formatter(
            pct,
        ):

            if pct < 4:

                return ""

            return f"{pct:.1f}%"

        return formatter

    # =====================================================
    # CASH FLOW CHART
    # =====================================================
    def cashflow_chart(
        self,
        monthly_trends: list[dict[str, Any]],
    ) -> str:
        """
        Generate a professional Monthly Cash Flow chart.

        Plots:
            • Income
            • Expense
            • Cash Flow

        Returns
        -------
        str
            Path to generated PNG chart.
        """

        if not monthly_trends:

            logger.warning(
                "No monthly cash flow data available."
            )

            return self._empty_chart(
                "No Cash Flow Data"
            )

        months = []
        income = []
        expense = []
        cashflow = []

        for row in monthly_trends:

            month = str(
                row.get(
                    "month",
                    "",
                )
            )

            months.append(
                self._wrap(
                    month,
                    10,
                )
            )

            inc = float(
                row.get(
                    "income",
                    0,
                )
                or 0
            )

            exp = float(
                row.get(
                    "expense",
                    0,
                )
                or 0
            )

            flow = float(

                row.get(

                    "cashflow",

                    inc - exp,

                )

                or 0

            )

            income.append(
                inc
            )

            expense.append(
                exp
            )

            cashflow.append(
                flow
            )

        fig, ax = self._create_figure()

        # -------------------------------------------------
        # Income
        # -------------------------------------------------

        ax.plot(

            months,

            income,

            color=COLOR_INCOME,

            linewidth=3,

            marker="o",

            markersize=7,

            label="Income",

        )

        # -------------------------------------------------
        # Expense
        # -------------------------------------------------

        ax.plot(

            months,

            expense,

            color=COLOR_EXPENSE,

            linewidth=3,

            marker="o",

            markersize=7,

            label="Expense",

        )

        # -------------------------------------------------
        # Cash Flow
        # -------------------------------------------------

        ax.plot(

            months,

            cashflow,

            color=COLOR_CASHFLOW,

            linewidth=2.8,

            linestyle="--",

            marker="D",

            markersize=6,

            label="Cash Flow",

        )

        # -------------------------------------------------
        # Dynamic Limits
        # -------------------------------------------------

        values = (
            income
            + expense
            + cashflow
        )

        minimum = min(values)

        maximum = max(values)

        padding = max(

            abs(
                maximum - minimum
            ) * 0.10,

            1000,

        )

        ax.set_ylim(

            minimum - padding,

            maximum + padding,

        )

        # -------------------------------------------------
        # Labels
        # -------------------------------------------------

        self._style_axis(

            ax,

            "Monthly Cash Flow Analysis",

            "Amount (₹)",

        )

        plt.setp(

            ax.get_xticklabels(),

            rotation=25,

            ha="right",

        )

        ax.tick_params(

            axis="x",

            pad=8,

        )

        ax.legend(

            loc="upper center",

            bbox_to_anchor=(0.5, 1.08),

            ncol=3,

            frameon=False,

        )

        # -------------------------------------------------
        # Data Points
        # -------------------------------------------------

        for x, y in zip(
            months,
            income,
        ):

            ax.annotate(

                f"{y:,.0f}",

                (x, y),

                textcoords="offset points",

                xytext=(0, 8),

                ha="center",

                fontsize=8,

            )

        filename = self._new_filename(
            "cashflow"
        )

        logger.info(
            "Cash Flow chart generated successfully."
        )

        return self._save_chart(

            fig,

            filename,

        )

    # =====================================================
    # MONTHLY TREND CHART
    # =====================================================
        # =====================================================
    # MONTHLY TREND CHART
    # =====================================================

    def monthly_trend_chart(
        self,
        monthly_trends: list[dict[str, Any]],
    ) -> str:
        """
        Generate Monthly Income vs Expense chart.
        """

        if not monthly_trends:

            logger.warning(
                "No monthly trend data available."
            )

            return self._empty_chart(
                "No Monthly Trend Data"
            )

        import numpy as np

        months = []
        income = []
        expense = []

        for row in monthly_trends:

            months.append(

                self._wrap(

                    str(
                        row.get(
                            "month",
                            "",
                        )
                    ),

                    10,

                )

            )

            income.append(

                float(
                    row.get(
                        "income",
                        0,
                    )
                    or 0
                )

            )

            expense.append(

                float(
                    row.get(
                        "expense",
                        0,
                    )
                    or 0
                )

            )

        x = np.arange(len(months))

        width = 0.36

        fig, ax = self._create_figure()

        income_bars = ax.bar(

            x - width / 2,

            income,

            width,

            color=COLOR_INCOME,

            label="Income",

            zorder=3,

        )

        expense_bars = ax.bar(

            x + width / 2,

            expense,

            width,

            color=COLOR_EXPENSE,

            label="Expense",

            zorder=3,

        )

        ax.set_xticks(x)

        ax.set_xticklabels(
            months
        )

        plt.setp(

            ax.get_xticklabels(),

            rotation=20,

            ha="right",

        )

        self._style_axis(

            ax,

            "Monthly Income vs Expense",

            "Amount (₹)",

        )

        values = income + expense

        if values:

            minimum = min(values)

            maximum = max(values)

            padding = max(

                (maximum - minimum) * 0.10,

                1000,

            )

            ax.set_ylim(

                max(
                    0,
                    minimum - padding,
                ),

                maximum + padding,

            )

        ax.legend(

            loc="upper center",

            bbox_to_anchor=(0.5, 1.08),

            ncol=2,

            frameon=False,

        )

        def annotate(
            bars,
        ):

            for bar in bars:

                value = bar.get_height()

                if value <= 0:

                    continue

                ax.annotate(

                    f"{value:,.0f}",

                    xy=(

                        bar.get_x()
                        + bar.get_width() / 2,

                        value,

                    ),

                    xytext=(0, 4),

                    textcoords="offset points",

                    ha="center",

                    va="bottom",

                    fontsize=8,

                )

        annotate(
            income_bars
        )

        annotate(
            expense_bars
        )

        filename = self._new_filename(
            "monthly_trend"
        )

        logger.info(
            "Monthly Trend chart generated successfully."
        )

        return self._save_chart(

            fig,

            filename,

        )

    # =====================================================
    # EXPENSE DISTRIBUTION CHART
    # =====================================================
        # =====================================================
    # EXPENSE DISTRIBUTION CHART
    # =====================================================

    def expense_pie_chart(
        self,
        categories: list[dict[str, Any]],
    ) -> str:
        """
        Generate Expense Distribution pie chart.
        """

        if not categories:

            logger.warning(
                "No expense category data available."
            )

            return self._empty_chart(
                "No Expense Data"
            )

        labels = []
        values = []

        for item in categories:

            amount = float(
                item.get(
                    "amount",
                    0,
                ) or 0
            )

            if amount <= 0:
                continue

            labels.append(

                self._wrap(

                    str(
                        item.get(
                            "category",
                            "Other",
                        )
                    ),

                    16,

                )

            )

            values.append(amount)

        if not values:

            return self._empty_chart(
                "No Expense Data"
            )

        fig, ax = self._create_figure(

            PIE_WIDTH,

            PIE_HEIGHT,

        )

        wedges, _, autotexts = ax.pie(

            values,

            startangle=90,

            colors=CHART_COLORS[:len(values)],

            autopct=self._autopct(values),

            pctdistance=0.72,

            labeldistance=1.08,

            wedgeprops={

                "linewidth": 1.2,

                "edgecolor": "white",

            },

        )

        for text in autotexts:

            text.set_fontsize(9)

            text.set_fontweight("bold")

            text.set_color("white")

        ax.legend(

            wedges,

            labels,

            title="Categories",

            loc="center left",

            bbox_to_anchor=(1.02, 0.5),

            frameon=False,

            fontsize=10,

            title_fontsize=11,

        )

        ax.set_title(

            "Expense Distribution",

            pad=20,

            fontweight="bold",

        )

        ax.axis("equal")

        filename = self._new_filename(
            "expense_pie"
        )

        logger.info(
            "Expense Distribution chart generated successfully."
        )

        return self._save_chart(

            fig,

            filename,

        )

    # =====================================================
    # SMART ALLOCATION CHART
    # =====================================================
        # =====================================================
    # SMART ALLOCATION CHART
    # =====================================================

    def allocation_chart(
        self,
        allocations: list[dict[str, Any]],
    ) -> str:
        """
        Generate Smart Financial Allocation
        doughnut chart.
        """

        if not allocations:

            logger.warning(
                "No allocation data available."
            )

            return self._empty_chart(
                "No Allocation Data"
            )

        labels = []
        values = []

        for item in allocations:

            amount = float(
                item.get(
                    "amount",
                    0,
                ) or 0
            )

            if amount <= 0:
                continue

            labels.append(

                self._wrap(

                    str(
                        item.get(
                            "name",
                            "Other",
                        )
                    ),

                    16,

                )

            )

            values.append(amount)

        if not values:

            return self._empty_chart(
                "No Allocation Data"
            )

        fig, ax = self._create_figure(

            PIE_WIDTH,

            PIE_HEIGHT,

        )

        wedges, _, autotexts = ax.pie(

            values,

            startangle=90,

            colors=CHART_COLORS[:len(values)],

            autopct=self._autopct(values),

            pctdistance=0.78,

            labeldistance=1.08,

            wedgeprops={

                "width": 0.42,

                "edgecolor": "white",

                "linewidth": 1.2,

            },

        )

        for text in autotexts:

            text.set_fontsize(9)

            text.set_fontweight("bold")

            text.set_color("white")

        centre_circle = plt.Circle(

            (0, 0),

            0.58,

            fc="white",

        )

        ax.add_artist(
            centre_circle
        )

        ax.text(

            0,

            0,

            "100%",

            ha="center",

            va="center",

            fontsize=15,

            fontweight="bold",

            color="#444444",

        )

        ax.legend(

            wedges,

            labels,

            title="Recommended Allocation",

            loc="center left",

            bbox_to_anchor=(1.02, 0.5),

            frameon=False,

            fontsize=10,

            title_fontsize=11,

        )

        ax.set_title(

            "Recommended Investment Allocation",

            pad=20,

            fontweight="bold",

        )

        ax.axis("equal")

        filename = self._new_filename(
            "allocation"
        )

        logger.info(
            "Allocation chart generated successfully."
        )

        return self._save_chart(

            fig,

            filename,

        )

    # =====================================================
    # GENERATE ALL CHARTS
    # =====================================================
        # =====================================================
    # GENERATE ALL CHARTS
    # =====================================================

    def generate_all(
        self,
        report_data: dict[str, Any],
    ) -> dict[str, str]:
        """
        Generate every report chart.
        """

        logger.info(
            "Generating all report charts..."
        )

        charts: dict[str, str] = {}

        # -------------------------------------------------
        # Cash Flow
        # -------------------------------------------------

        try:

            charts["cashflow_chart"] = self.cashflow_chart(

                report_data.get(
                    "monthly_trends",
                    [],
                )

            )

        except Exception:

            logger.exception(
                "Cash Flow chart generation failed."
            )

            charts["cashflow_chart"] = self._empty_chart(
                "Cash Flow Unavailable"
            )

        # -------------------------------------------------
        # Monthly Trend
        # -------------------------------------------------

        try:

            charts["monthly_trend_chart"] = self.monthly_trend_chart(

                report_data.get(
                    "monthly_trends",
                    [],
                )

            )

        except Exception:

            logger.exception(
                "Monthly Trend chart generation failed."
            )

            charts["monthly_trend_chart"] = self._empty_chart(
                "Monthly Trend Unavailable"
            )

        # -------------------------------------------------
        # Expense Distribution
        # -------------------------------------------------

        try:

            categories = (

                report_data.get(
                    "category_breakdown",
                    {},
                ).get(
                    "categories",
                    [],
                )

            )

            charts["expense_distribution_chart"] = (

                self.expense_pie_chart(
                    categories
                )

            )

        except Exception:

            logger.exception(
                "Expense Distribution chart generation failed."
            )

            charts["expense_distribution_chart"] = (

                self._empty_chart(
                    "Expense Distribution Unavailable"
                )

            )

        # -------------------------------------------------
        # Allocation
        # -------------------------------------------------

        try:

            allocations = (

                report_data.get(
                    "allocation",
                    {},
                ).get(
                    "allocations",
                    [],
                )

            )

            charts["allocation_chart"] = (

                self.allocation_chart(
                    allocations
                )

            )

        except Exception:

            logger.exception(
                "Allocation chart generation failed."
            )

            charts["allocation_chart"] = (

                self._empty_chart(
                    "Allocation Unavailable"
                )

            )

        logger.info(

            "%d chart(s) generated successfully.",

            len(charts),

        )

        return charts

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup(
        self,
    ) -> None:
        """
        Delete generated PNG files.
        Safe to call multiple times.
        """

        if not self.output_dir.exists():

            return

        deleted = 0
        failed = 0

        for image in self.output_dir.glob("*.png"):

            try:

                image.unlink()

                deleted += 1

            except Exception:

                failed += 1

                logger.exception(

                    "Unable to delete %s",

                    image,

                )

        logger.info(

            "Chart cleanup complete (deleted=%d, failed=%d)",

            deleted,

            failed,

        )

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_report_data(
        self,
        report_data: dict[str, Any],
    ) -> bool:
        """
        Validate report data before
        chart generation.
        """

        if not isinstance(
            report_data,
            dict,
        ):

            logger.error(
                "Report data must be a dictionary."
            )

            return False

        if not report_data:

            logger.error(
                "Report data is empty."
            )

            return False

        required = [

            "monthly_trends",

            "category_breakdown",

            "allocation",

        ]

        missing = [

            key

            for key in required

            if key not in report_data

        ]

        if missing:

            logger.warning(

                "Missing report sections: %s",

                ", ".join(missing),

            )

        return True

    # =====================================================
    # PUBLIC ENTRY
    # =====================================================

    def create(
        self,
        report_data: dict[str, Any],
    ) -> dict[str, str]:
        """
        Validate report data and
        generate every chart.
        """

        if not self.validate_report_data(
            report_data
        ):

            raise ValueError(
                "Invalid report data supplied."
            )

        try:

            charts = self.generate_all(
                report_data
            )

            logger.info(

                "Successfully generated %d chart(s).",

                len(charts),

            )

            return charts

        except Exception:

            logger.exception(
                "Chart generation failed."
            )

            self.cleanup()

            raise