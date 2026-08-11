"""
==========================================================
Finacle AI
Financial Insight Engine
==========================================================

Generates intelligent financial insights for the PDF report.

Uses:
    ReportData

Returns:
    AI recommendations
    Spending analysis
    Savings analysis
    Cash flow analysis
    Final conclusion
"""

from services.report_data import ReportData


class ReportAI:

    """
    Generates AI-powered financial insights.
    """

    # =====================================================
    # Spending Insight
    # =====================================================

    @staticmethod
    def spending(report: ReportData):

        if report.total_income == 0:

            return (
                "No income records were found during the selected "
                "reporting period."
            )

        ratio = report.expense_ratio

        if ratio < 40:

            return (
                f"You spent only {ratio:.1f}% of your income. "
                "This indicates excellent spending discipline."
            )

        elif ratio < 70:

            return (
                f"You spent {ratio:.1f}% of your income. "
                "Your spending remains balanced."
            )

        elif ratio < 90:

            return (
                f"Expenses account for {ratio:.1f}% of your income. "
                "There is still room to improve monthly savings."
            )

        return (
            f"Almost your entire income ({ratio:.1f}%) was spent. "
            "Reducing discretionary expenses is recommended."
        )

    # =====================================================
    # Savings Insight
    # =====================================================

    @staticmethod
    def savings(report: ReportData):

        rate = report.savings_rate

        if rate >= 50:

            return (
                f"You save {rate:.1f}% of your income. "
                "This is an outstanding savings rate."
            )

        elif rate >= 30:

            return (
                f"Your savings rate is {rate:.1f}%. "
                "Your financial habits are healthy."
            )

        elif rate >= 15:

            return (
                f"Your savings rate is {rate:.1f}%. "
                "Increasing investments can improve long-term wealth."
            )

        return (
            f"Only {rate:.1f}% of your income is currently saved. "
            "Consider reviewing recurring expenses."
        )

    # =====================================================
    # Cash Flow
    # =====================================================

    @staticmethod
    def cashflow(report: ReportData):

        if report.cash_flow == "Positive":

            return (
                "Your income exceeded your expenses during this "
                "reporting period, resulting in a positive cash flow."
            )

        return (
            "Your expenses exceeded your income. "
            "Budget optimisation is recommended."
        )

    # =====================================================
    # Category Insight
    # =====================================================

    @staticmethod
    def category(report: ReportData):

        if report.highest_category is None:

            return (
                "No expense categories were available for analysis."
            )

        return (

            f"The highest spending category was "

            f"'{report.highest_category}', "

            f"with a total expenditure of "

            f"₹{report.highest_category_amount:,.2f}."

        )

    # =====================================================
    # Recommendation Engine
    # =====================================================

    @staticmethod
    def recommendations(report: ReportData):

        recommendations = []

        if report.savings_rate < 20:

            recommendations.append(
                "Increase your monthly savings target."
            )

        if report.cash_flow == "Negative":

            recommendations.append(
                "Reduce recurring expenses to restore positive cash flow."
            )

        if report.highest_category_amount > report.total_income * 0.40:

            recommendations.append(
                f"Review spending in '{report.highest_category}'."
            )

        if report.savings_rate >= 30:

            recommendations.append(
                "Consider investing surplus funds in SIPs, Index Funds or PPF."
            )

        if report.transaction_count < 10:

            recommendations.append(
                "Track transactions more consistently for better insights."
            )

        if not recommendations:

            recommendations.append(
                "Continue your current financial habits."
            )

        return recommendations

    # =====================================================
    # Financial Rating
    # =====================================================

    @staticmethod
    def rating(report: ReportData):

        score = 0

        if report.cash_flow == "Positive":
            score += 30

        if report.savings_rate >= 20:
            score += 25

        if report.savings_rate >= 40:
            score += 20

        if report.transaction_count >= 20:
            score += 15

        if report.highest_category_amount < report.total_income * 0.30:
            score += 10

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "Very Good"

        elif score >= 60:
            return "Good"

        elif score >= 40:
            return "Average"

        return "Needs Improvement"

    # =====================================================
    # Conclusion
    # =====================================================

    @staticmethod
    def conclusion(report: ReportData):

        rating = ReportAI.rating(report)

        if rating == "Excellent":

            return (
                "Your financial profile reflects disciplined spending, "
                "strong savings, and healthy cash flow. "
                "Maintaining this consistency while increasing investments "
                "can significantly improve long-term wealth creation."
            )

        elif rating == "Very Good":

            return (
                "Your finances remain healthy. "
                "Minor improvements in savings and investment planning "
                "can further strengthen your financial position."
            )

        elif rating == "Good":

            return (
                "Your financial performance is stable. "
                "Reducing discretionary expenses and increasing savings "
                "will improve future financial security."
            )

        elif rating == "Average":

            return (
                "Your finances require closer monitoring. "
                "Preparing a monthly budget and controlling expenses "
                "will improve overall stability."
            )

        return (
            "Your spending currently exceeds recommended levels. "
            "Focus on budgeting, building an emergency fund, and "
            "reducing unnecessary expenses."
        )

    # =====================================================
    # Build Complete AI Report
    # =====================================================

    @staticmethod
    def generate(report: ReportData):

        return {

            "rating": ReportAI.rating(report),

            "spending": ReportAI.spending(report),

            "savings": ReportAI.savings(report),

            "cashflow": ReportAI.cashflow(report),

            "category": ReportAI.category(report),

            "recommendations": ReportAI.recommendations(report),

            "conclusion": ReportAI.conclusion(report)

        }