from typing import Dict, List


class FutureFinancialSimulator:

    def __init__(
        self,
        monthly_income,
        monthly_expense,
        monthly_investment,
        annual_return,
        salary_growth,
        inflation,
        years
    ):

        self.monthly_income = float(monthly_income or 0)
        self.monthly_expense = float(monthly_expense or 0)
        self.monthly_investment = float(monthly_investment or 0)

        self.annual_return = float(annual_return or 12)
        self.salary_growth = float(salary_growth or 8)
        self.inflation = float(inflation or 6)

        self.years = int(years or 5)

    # ======================================================
    # Future Financial Simulation
    # ======================================================

    def simulate(self) -> Dict:

        monthly_rate = (self.annual_return / 100) / 12

        current_income = self.monthly_income
        current_expense = self.monthly_expense

        total_invested = 0.0
        portfolio_value = 0.0

        yearly_growth: List[Dict] = []

        for year in range(1, self.years + 1):

            yearly_income = current_income * 12
            yearly_expense = current_expense * 12

            yearly_investment = self.monthly_investment * 12

            total_invested += yearly_investment

            for _ in range(12):
                portfolio_value *= (1 + monthly_rate)
                portfolio_value += self.monthly_investment

            yearly_growth.append({

                "year": year,

                "income": round(yearly_income),

                "expense": round(yearly_expense),

                "investment": round(total_invested),

                "portfolio": round(portfolio_value)

            })

            current_income *= (1 + (self.salary_growth / 100))
            current_expense *= (1 + (self.inflation / 100))

        total_returns = portfolio_value - total_invested

        net_worth = portfolio_value

        inflation_adjusted = portfolio_value / (
            (1 + self.inflation / 100) ** self.years
        )

        # ==================================================
        # Savings Rate
        # ==================================================

        savings = max(
            self.monthly_income -
            self.monthly_expense,
            0
        )

        if self.monthly_income > 0:

            savings_rate = (
                savings /
                self.monthly_income
            ) * 100

        else:

            savings_rate = 0

        # ==================================================
        # Goal Probability
        # ==================================================

        if savings_rate >= 40:

            goal_probability = "Very High"

        elif savings_rate >= 25:

            goal_probability = "High"

        elif savings_rate >= 15:

            goal_probability = "Moderate"

        else:

            goal_probability = "Low"

        # ==================================================
        # AI Insights
        # ==================================================

        advice = []

        if savings_rate < 20:

            advice.append(
                "Increase your monthly savings to improve future wealth."
            )

        if self.monthly_investment == 0:

            advice.append(
                "Start a monthly SIP to benefit from compounding."
            )

        if self.annual_return < 8:

            advice.append(
                "Expected annual return is conservative. Consider diversified investments."
            )

        if self.salary_growth < self.inflation:

            advice.append(
                "Salary growth is below inflation. Purchasing power may decrease."
            )

        if self.years >= 10:

            advice.append(
                "Long-term investing significantly improves wealth creation."
            )

        if not advice:

            advice.append(
                "Your financial plan looks healthy. Continue investing consistently."
            )

        # ==================================================
        # Return
        # ==================================================

        return {

            "monthly_income": round(self.monthly_income),

            "monthly_expense": round(self.monthly_expense),

            "monthly_investment": round(self.monthly_investment),

            "annual_return": self.annual_return,

            "salary_growth": self.salary_growth,

            "inflation": self.inflation,

            "years": self.years,

            "total_invested": round(total_invested),

            "future_value": round(portfolio_value),

            "total_returns": round(total_returns),

            "net_worth": round(net_worth),

            "inflation_adjusted_value": round(inflation_adjusted),

            "saving_rate": round(savings_rate, 1),

            "goal_probability": goal_probability,

            "yearly_growth": yearly_growth,

            "ai_advice": advice

        }