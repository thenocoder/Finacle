"""
==============================================================
Finacle - Report Data Service
==============================================================

Builds the complete financial dataset consumed by:

• Dashboard
• PDF Reports
• APIs

This module performs calculations only.
It does NOT render templates or generate PDFs.
"""

from __future__ import annotations

import logging

from collections import defaultdict
from datetime import datetime
from statistics import mean
from typing import Any

from sqlalchemy import func

from extensions import db

from models.user import User
from models.transaction import Transaction
from models.financial_profile import FinancialProfile

from services.expense_predictor import ExpensePredictor
from services.allocation_engine import AllocationEngine


# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# CONSTANTS
# ==========================================================

INCOME = "Income"
EXPENSE = "Expense"


# ==========================================================
# REPORT DATA SERVICE
# ==========================================================

class ReportDataService:
    """
    Builds the complete reporting dataset.

    This class performs calculations only.

    Every dashboard widget, PDF page and API
    consumes the dictionary returned by
    build_report().
    """

    # ======================================================
    # CONSTRUCTOR
    # ======================================================

    def __init__(
        self,
        user_id: int,
    ) -> None:

        self.user_id = user_id

        logger.info(
            "Initializing ReportDataService for user %s",
            user_id,
        )

        self.user = self._load_user()

        self.profile = self._load_profile()

        self.transactions = self._load_transactions()

    # ======================================================
    # DATABASE LOADERS
    # ======================================================

    def _load_user(self) -> User:
        """
        Load current user.
        """

        user = User.query.get(
            self.user_id
        )

        if user is None:

            raise ValueError(
                f"User {self.user_id} does not exist."
            )

        return user

    # ------------------------------------------------------

    def _load_profile(
        self,
    ) -> FinancialProfile | None:
        """
        Load the user's financial profile.
        """

        return (
            FinancialProfile.query
            .filter_by(
                user_id=self.user_id
            )
            .first()
        )

    # ------------------------------------------------------

    def _load_transactions(
        self,
    ) -> list[Transaction]:
        """
        Load every transaction ordered by date.
        """

        transactions = (
            Transaction.query
            .filter_by(
                user_id=self.user_id
            )
            .order_by(
                Transaction.date.asc()
            )
            .all()
        )

        logger.info(
            "Loaded %d transaction(s).",
            len(transactions),
        )

        return transactions

    # ======================================================
    # HELPER METHODS
    # ======================================================

    @staticmethod
    def _round(
        value: Any,
    ) -> float:
        """
        Safely round numeric values.
        """

        try:

            return round(
                float(value or 0),
                2,
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # ------------------------------------------------------

    @staticmethod
    def _currency(
        value: Any,
    ) -> float:
        """
        Normalize currency values.
        """

        try:

            return float(
                value or 0
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # ------------------------------------------------------

    @staticmethod
    def _safe_percentage(
        value: float,
        total: float,
    ) -> float:
        """
        Calculate percentages safely.
        """

        if total <= 0:

            return 0.0

        return round(
            (value / total) * 100,
            2,
        )

    # ------------------------------------------------------

    @staticmethod
    def _month_key(
        date,
    ) -> str:
        """
        Convert a date into
        a monthly grouping key.
        """

        return date.strftime(
            "%b %Y"
        )

    # ======================================================
    # FINANCIAL SUMMARY
    # ======================================================
        # ======================================================
    # FINANCIAL SUMMARY
    # ======================================================

    def _calculate_summary(
        self,
    ) -> dict[str, float]:
        """
        Calculate the overall financial summary.
        """

        income = 0.0
        expense = 0.0

        income_count = 0
        expense_count = 0

        for tx in self.transactions:

            amount = self._currency(
                tx.amount
            )

            if tx.type == INCOME:

                income += amount
                income_count += 1

            elif tx.type == EXPENSE:

                expense += amount
                expense_count += 1

        other_income = 0.0

        if self.profile:

            other_income = self._currency(
                getattr(
                    self.profile,
                    "monthly_other_income",
                    0,
                )
            )

        total_income = (
            income + other_income
        )

        savings = (
            total_income - expense
        )

        saving_rate = self._safe_percentage(
            savings,
            total_income,
        )

        return {

            "income": self._round(
                total_income
            ),

            "transaction_income": self._round(
                income
            ),

            "other_income": self._round(
                other_income
            ),

            "expense": self._round(
                expense
            ),

            "savings": self._round(
                savings
            ),

            "saving_rate": saving_rate,

            "income_count": income_count,

            "expense_count": expense_count,

        }

    # ======================================================
    # MONTHLY TRENDS
    # ======================================================

    def _monthly_trends(
        self,
    ) -> list[dict[str, Any]]:
        """
        Build monthly income,
        expense and cashflow data.
        """

        monthly = defaultdict(
            lambda: {

                "income": 0.0,

                "expense": 0.0,

            }
        )

        for tx in self.transactions:

            key = self._month_key(
                tx.date
            )

            amount = self._currency(
                tx.amount
            )

            if tx.type == INCOME:

                monthly[key][
                    "income"
                ] += amount

            elif tx.type == EXPENSE:

                monthly[key][
                    "expense"
                ] += amount

        trends = []

        for month, values in monthly.items():

            income = values["income"]

            expense = values["expense"]

            trends.append({

                "month": month,

                "income": self._round(
                    income
                ),

                "expense": self._round(
                    expense
                ),

                "cashflow": self._round(
                    income - expense
                ),

            })

        return trends

    # ======================================================
    # CATEGORY BREAKDOWN
    # ======================================================

    def _category_breakdown(
        self,
    ) -> dict[str, Any]:
        """
        Build expense category distribution.
        """

        categories = defaultdict(
            float
        )

        total_expense = 0.0

        for tx in self.transactions:

            if tx.type != EXPENSE:

                continue

            category = (
                tx.category
                or "Uncategorized"
            )

            amount = self._currency(
                tx.amount
            )

            categories[
                category
            ] += amount

            total_expense += amount

        breakdown = []

        for category, amount in sorted(

            categories.items(),

            key=lambda item: item[1],

            reverse=True,

        ):

            breakdown.append({

                "category": category,

                "amount": self._round(
                    amount
                ),

                "percentage": self._safe_percentage(
                    amount,
                    total_expense,
                ),

            })

        return {

            "total": self._round(
                total_expense
            ),

            "categories": breakdown,

        }
            # ======================================================
    # CASHFLOW ANALYSIS
    # ======================================================

    def _cashflow_analysis(
        self,
    ) -> dict[str, Any]:
        """
        Analyze the user's overall cashflow health.
        """

        summary = self._calculate_summary()

        income = summary["income"]
        expense = summary["expense"]
        savings = summary["savings"]

        if income <= 0:

            status = "No Income"

        elif savings < 0:

            status = "Negative"

        elif savings == 0:

            status = "Break Even"

        elif summary["saving_rate"] >= 30:

            status = "Healthy"

        else:

            status = "Moderate"

        return {

            "income": self._round(
                income
            ),

            "expense": self._round(
                expense
            ),

            "cashflow": self._round(
                savings
            ),

            "saving_rate": summary[
                "saving_rate"
            ],

            "status": status,

        }

    # ======================================================
    # LARGEST EXPENSES
    # ======================================================

    def _largest_expenses(
        self,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Return the largest expense transactions.
        """

        expenses = sorted(

            (
                tx
                for tx in self.transactions
                if tx.type == EXPENSE
            ),

            key=lambda tx: self._currency(
                tx.amount
            ),

            reverse=True,

        )

        results = []

        for tx in expenses[:limit]:

            results.append({

                "title": tx.title,

                "category": (
                    tx.category
                    or "Uncategorized"
                ),

                "amount": self._round(
                    tx.amount
                ),

                "payment_method": (
                    tx.payment_method
                    or "-"
                ),

                "date": tx.date.strftime(
                    "%d %b %Y"
                ),

            })

        return results

    # ======================================================
    # MONTHLY STATISTICS
    # ======================================================

    def _monthly_statistics(
        self,
    ) -> dict[str, float]:
        """
        Calculate monthly financial statistics.
        """

        monthly = self._monthly_trends()

        if not monthly:

            return {

                "highest_income": 0,

                "highest_expense": 0,

                "average_income": 0,

                "average_expense": 0,

                "average_cashflow": 0,

            }

        incomes = [

            month["income"]

            for month in monthly

        ]

        expenses = [

            month["expense"]

            for month in monthly

        ]

        cashflows = [

            month["cashflow"]

            for month in monthly

        ]

        return {

            "highest_income": self._round(
                max(incomes)
            ),

            "highest_expense": self._round(
                max(expenses)
            ),

            "average_income": self._round(
                mean(incomes)
            ),

            "average_expense": self._round(
                mean(expenses)
            ),

            "average_cashflow": self._round(
                mean(cashflows)
            ),

        }

    # ======================================================
    # SPENDING BEHAVIOUR
    # ======================================================
        # ======================================================
    # SPENDING BEHAVIOUR
    # ======================================================

    def _spending_behaviour(
        self,
    ) -> dict[str, Any]:
        """
        Analyze the user's spending behaviour.
        """

        category_data = self._category_breakdown()

        summary = self._calculate_summary()

        categories = category_data["categories"]

        if not categories:

            return {

                "primary_category": "N/A",

                "largest_percentage": 0,

                "expense_ratio": 0,

                "behaviour": "No Data",

            }

        primary = categories[0]

        expense_ratio = self._safe_percentage(

            summary["expense"],

            summary["income"],

        )

        if expense_ratio >= 90:

            behaviour = "Overspending"

        elif expense_ratio >= 70:

            behaviour = "Needs Improvement"

        elif expense_ratio >= 50:

            behaviour = "Balanced"

        else:

            behaviour = "Excellent"

        return {

            "primary_category": primary["category"],

            "largest_percentage": primary["percentage"],

            "expense_ratio": expense_ratio,

            "behaviour": behaviour,

        }

    # ======================================================
    # EXPENSE DISTRIBUTION
    # ======================================================

    def _expense_distribution(
        self,
    ) -> dict[str, float]:
        """
        Build category → amount mapping
        used by charts.
        """

        breakdown = self._category_breakdown()

        return {

            item["category"]: item["amount"]

            for item in breakdown["categories"]

        }

    # ======================================================
    # FINANCIAL HEALTH SCORE
    # ======================================================

    def _financial_score(
        self,
    ) -> dict[str, Any]:
        """
        Calculate the overall financial
        health score.
        """

        summary = self._calculate_summary()

        behaviour = self._spending_behaviour()

        score = 0

        # --------------------------------------------------
        # Saving Rate (35 Marks)
        # --------------------------------------------------

        saving_rate = summary["saving_rate"]

        if saving_rate >= 40:

            score += 35

        elif saving_rate >= 30:

            score += 30

        elif saving_rate >= 20:

            score += 22

        elif saving_rate >= 10:

            score += 12

        else:

            score += 5

        # --------------------------------------------------
        # Expense Ratio (20 Marks)
        # --------------------------------------------------

        expense_ratio = self._safe_percentage(

            summary["expense"],

            summary["income"],

        )

        if expense_ratio <= 50:

            score += 20

        elif expense_ratio <= 70:

            score += 15

        elif expense_ratio <= 90:

            score += 8

        else:

            score += 2

        # --------------------------------------------------
        # Emergency Fund (15 Marks)
        # --------------------------------------------------

        if self.profile:

            if getattr(

                self.profile,

                "emergency_fund_available",

                False,

            ):

                score += 15

            elif getattr(

                self.profile,

                "emergency_fund_months",

                0,

            ) >= 3:

                score += 10

        # --------------------------------------------------
        # Investments (15 Marks)
        # --------------------------------------------------

        if self.profile:

            investments = [

                getattr(
                    self.profile,
                    "sip",
                    False,
                ),

                getattr(
                    self.profile,
                    "stocks",
                    False,
                ),

                getattr(
                    self.profile,
                    "mutual_funds",
                    False,
                ),

                getattr(
                    self.profile,
                    "gold",
                    False,
                ),

                getattr(
                    self.profile,
                    "ppf",
                    False,
                ),

                getattr(
                    self.profile,
                    "nps",
                    False,
                ),

                getattr(
                    self.profile,
                    "fd",
                    False,
                ),

                getattr(
                    self.profile,
                    "lic",
                    False,
                ),

            ]

            score += min(

                sum(

                    bool(item)

                    for item in investments

                ) * 3,

                15,

            )

        # --------------------------------------------------
        # Spending Behaviour (15 Marks)
        # --------------------------------------------------

        behaviour_score = {

            "Excellent": 15,

            "Balanced": 12,

            "Needs Improvement": 8,

            "Overspending": 3,

            "No Data": 0,

        }

        score += behaviour_score.get(

            behaviour["behaviour"],

            0,

        )

        score = min(

            score,

            100,

        )

        # --------------------------------------------------
        # Grade
        # --------------------------------------------------

        if score >= 90:

            grade = "A+"

            status = "Outstanding"

        elif score >= 80:

            grade = "A"

            status = "Excellent"

        elif score >= 70:

            grade = "B"

            status = "Good"

        elif score >= 60:

            grade = "C"

            status = "Average"

        else:

            grade = "D"

            status = "Needs Improvement"

        return {

            "score": score,

            "grade": grade,

            "status": status,

        }

    # ======================================================
    # FINANCIAL DNA
    # ======================================================
        # ======================================================
    # FINANCIAL DNA
    # ======================================================

    def _financial_dna(
        self,
    ) -> dict[str, Any]:
        """
        Build the user's financial DNA profile.
        """

        if not self.profile:

            return {

                "risk_profile": "Unknown",

                "goal": "Unknown",

                "investment_horizon": "Unknown",

                "spender_type": "Unknown",

                "investor_type": "Unknown",

            }

        behaviour = self._spending_behaviour()

        ratio = behaviour["expense_ratio"]

        if ratio >= 90:

            spender = "Aggressive Spender"

        elif ratio >= 70:

            spender = "Lifestyle Spender"

        elif ratio >= 50:

            spender = "Balanced Spender"

        else:

            spender = "Smart Saver"

        investor_map = {

            "Low": "Conservative",

            "Medium": "Balanced",

            "High": "Growth",

        }

        return {

            "risk_profile": self.profile.risk_appetite,

            "goal": self.profile.financial_goal,

            "investment_horizon": self.profile.investment_horizon,

            "spender_type": spender,

            "investor_type": investor_map.get(

                self.profile.risk_appetite,

                "Balanced",

            ),

        }

    # ======================================================
    # EXPENSE PREDICTION
    # ======================================================

    def _prediction(
        self,
    ) -> dict[str, Any]:
        """
        Build standardized prediction data.
        """

        predictor = ExpensePredictor(
            self.transactions
        )

        raw = predictor.predict()

        summary = self._calculate_summary()

        predicted = self._round(

            raw.get(

                "prediction",

                raw.get(

                    "predicted_expense",

                    0,

                ),

            )

        )

        expected_savings = max(

            0,

            summary["income"] - predicted,

        )

        return {

            "predicted_expense": predicted,

            "expected_savings": self._round(
                expected_savings
            ),

            "confidence": raw.get(
                "confidence",
                85,
            ),

            "trend": raw.get(
                "trend",
                "Stable",
            ),

        }

    # ======================================================
    # SMART ALLOCATION
    # ======================================================

    def _allocation(
        self,
    ) -> dict[str, Any]:
        """
        Generate investment allocation.
        """

        summary = self._calculate_summary()

        if not self.profile:

            return {

                "income": summary["income"],

                "expense": summary["expense"],

                "available_savings": summary["savings"],

                "allocations": [],

                "advice": [

                    "Complete your financial profile to receive personalized allocation."

                ],

            }

        engine = AllocationEngine(

            summary["income"],

            summary["expense"],

            self.profile,

        )

        raw = engine.generate()

        allocations = []

        allocation_data = raw.get(
            "allocation",
            {},
        )

        for name, amount in allocation_data.items():

            allocations.append({

                "name": name,

                "amount": self._round(
                    amount
                ),

            })

        return {

            "income": summary["income"],

            "expense": summary["expense"],

            "available_savings": summary["savings"],

            "allocations": allocations,

            "advice": raw.get(
                "advice",
                [],
            ),

        }

    # ======================================================
    # AI RECOMMENDATIONS
    # ======================================================

    def _recommendations(
        self,
    ) -> list[str]:
        """
        Generate personalized recommendations.
        """

        summary = self._calculate_summary()

        behaviour = self._spending_behaviour()

        recommendations = []

        if summary["saving_rate"] < 20:

            recommendations.append(
                "Increase your monthly savings rate."
            )

        if behaviour["expense_ratio"] > 70:

            recommendations.append(
                "Reduce discretionary spending."
            )

        if self.profile is None:

            recommendations.append(
                "Complete your financial profile."
            )

        prediction = self._prediction()

        if prediction["trend"] == "Increasing":

            recommendations.append(
                "Your expenses are rising. Review recurring expenses."
            )

        if not recommendations:

            recommendations.append(
                "Maintain your current financial discipline."
            )

        return recommendations

    # ======================================================
    # FINANCIAL GOALS
    # ======================================================

    def _financial_goals(
        self,
    ) -> list[dict[str, Any]]:
        """
        Build financial goal progress.
        """

        if not self.profile:

            return []

        goals = []

        if getattr(

            self.profile,

            "financial_goal",

            None,

        ):

            goals.append({

                "title": self.profile.financial_goal,

                "progress": min(

                    self._financial_score()["score"],

                    100,

                ),

            })

        return goals

    # ======================================================
    # AI INSIGHTS
    # ======================================================

    def _insights(
        self,
    ) -> list[str]:
        """
        Generate executive insights.
        """

        summary = self._calculate_summary()

        prediction = self._prediction()

        behaviour = self._spending_behaviour()

        score = self._financial_score()

        insights = []

        if summary["saving_rate"] >= 30:

            insights.append(
                "Excellent savings rate."
            )

        elif summary["saving_rate"] < 15:

            insights.append(
                "Savings rate is below the recommended level."
            )

        insights.append(

            f"Highest spending category: {behaviour['primary_category']}."

        )

        insights.append(

            f"Predicted next month's expense: ₹{prediction['predicted_expense']:,.2f}."

        )

        insights.append(

            f"Financial health score: {score['score']}/100 ({score['grade']})."

        )

        if prediction["trend"] == "Increasing":

            insights.append(
                "Monthly expenses are increasing."
            )

        elif prediction["trend"] == "Decreasing":

            insights.append(
                "Monthly expenses are decreasing."
            )

        return insights

    # ======================================================
    # BUILD REPORT
    # ======================================================

    def build_report(
        self,
    ) -> dict[str, Any]:
        """
        Build the complete reporting dataset.
        """

        logger.info(
            "Building complete report dataset..."
        )

        summary = self._calculate_summary()

        report = {

            "generated_at": datetime.now().strftime(
                "%d %B %Y %I:%M %p"
            ),

            "generated_on": datetime.now(),

            "user": {

                "id": self.user.id,

                "name": self.user.name,

                "email": self.user.email,

            },

            "summary": summary,

            "cashflow": self._cashflow_analysis(),

            "monthly_trends": self._monthly_trends(),

            "category_breakdown": self._category_breakdown(),

            "expense_distribution": self._expense_distribution(),

            "monthly_statistics": self._monthly_statistics(),

            "spending_behaviour": self._spending_behaviour(),

            "largest_expenses": self._largest_expenses(),

            "prediction": self._prediction(),

            "allocation": self._allocation(),

            "recommendations": self._recommendations(),

            "financial_goals": self._financial_goals(),

            "financial_score": self._financial_score(),

            "financial_dna": self._financial_dna(),

            "insights": self._insights(),

            "transactions": [

                {

                    "id": tx.id,

                    "date": tx.date.strftime(
                        "%d %b %Y"
                    ),

                    "title": tx.title,

                    "category": tx.category,

                    "type": tx.type,

                    "payment_method": tx.payment_method,

                    "amount": self._round(
                        tx.amount
                    ),

                    "notes": tx.notes or "",

                }

                for tx in self.transactions

            ],

        }

        logger.info(
            "Report dataset built successfully."
        )

        return report

    # ======================================================
    # REFRESH
    # ======================================================
        # ======================================================
    # REFRESH
    # ======================================================

    def refresh(
        self,
    ) -> "ReportDataService":
        """
        Reload user, profile and transaction data.
        """

        db.session.expire_all()

        self.user = self._load_user()

        self.profile = self._load_profile()

        self.transactions = self._load_transactions()

        logger.info(
            "ReportDataService refreshed."
        )

        return self

    # ======================================================
    # REPORT SUMMARY
    # ======================================================

    def report_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return a lightweight report summary.
        """

        report = self.build_report()

        return {

            "user": report["user"]["name"],

            "income": report["summary"]["income"],

            "expense": report["summary"]["expense"],

            "savings": report["summary"]["savings"],

            "score": report["financial_score"]["score"],

            "prediction": report["prediction"]["predicted_expense"],

        }