from dataclasses import dataclass


@dataclass
class DashboardSummary:

    health_score: int

    savings_rate: float

    expense_ratio: float

    risk_level: str

    health_color: str

    recommendation: str

    status: str


class DashboardAnalytics:

    def __init__(

        self,

        income,

        expense,

        transactions

    ):

        self.income = income or 0

        self.expense = expense or 0

        self.transactions = transactions or 0

    # =====================================================
    # Main Generator
    # =====================================================

    def generate(self):

        savings = self.income - self.expense

        # -----------------------------------------------

        if self.income > 0:

            savings_rate = (

                savings / self.income

            ) * 100

            expense_ratio = (

                self.expense / self.income

            ) * 100

        else:

            savings_rate = 0

            expense_ratio = 100

        # -----------------------------------------------
        # Financial Health Score
        # -----------------------------------------------

        score = 100

        if expense_ratio > 90:

            score -= 40

        elif expense_ratio > 75:

            score -= 25

        elif expense_ratio > 60:

            score -= 15

        if savings_rate < 0:

            score -= 25

        elif savings_rate < 10:

            score -= 10

        if self.transactions > 100:

            score -= 5

        score = max(0, min(100, score))

        # -----------------------------------------------
        # Risk Level
        # -----------------------------------------------

        if score >= 80:

            risk = "Low"

            color = "success"

            status = "Excellent"

            recommendation = (

                "Your finances are in great shape. Continue investing consistently."

            )

        elif score >= 60:

            risk = "Moderate"

            color = "warning"

            status = "Good"

            recommendation = (

                "Reduce unnecessary expenses and improve your monthly savings."

            )

        else:

            risk = "High"

            color = "danger"

            status = "Needs Attention"

            recommendation = (

                "Your expenses are too high compared to your income. Focus on budgeting."

            )

        # -----------------------------------------------

        return DashboardSummary(

            health_score=score,

            savings_rate=round(

                savings_rate,

                2

            ),

            expense_ratio=round(

                expense_ratio,

                2

            ),

            risk_level=risk,

            health_color=color,

            recommendation=recommendation,

            status=status

        )