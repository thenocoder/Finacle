from typing import Dict, List


class SimulatorEngine:
    """
    Future Financial Simulator
    """

    def __init__(
        self,
        monthly_income: float,
        monthly_expense: float,
        monthly_investment: float,
        annual_return: float,
        years: int
    ):

        self.monthly_income = float(monthly_income or 0)
        self.monthly_expense = float(monthly_expense or 0)
        self.monthly_investment = float(monthly_investment or 0)
        self.annual_return = float(annual_return or 12)
        self.years = int(years or 10)

        # Default assumptions
        self.salary_growth = 8.0
        self.inflation = 6.0

    # ==========================================================
    # Future Simulation
    # ==========================================================

    def simulate(self) -> Dict:

        monthly_rate = (self.annual_return / 100) / 12

        balance = 0.0
        total_invested = 0.0

        yearly_growth: List[Dict] = []

        income = self.monthly_income
        expense = self.monthly_expense
        investment = self.monthly_investment

        for year in range(1, self.years + 1):

            for _ in range(12):

                balance = (
                    balance * (1 + monthly_rate)
                ) + investment

                total_invested += investment

            yearly_growth.append({

                "year": year,

                "income": round(income),

                "expense": round(expense),

                "investment": round(total_invested),

                "portfolio": round(balance)

            })

            income *= (1 + self.salary_growth / 100)
            expense *= (1 + self.inflation / 100)
            investment = max(income - expense, 0)

        future_value = round(balance)

        total_invested = round(total_invested)

        total_returns = future_value - total_invested

        inflation_adjusted_value = round(

            future_value /

            ((1 + self.inflation / 100) ** self.years)

        )

        saving_rate = round(

            (self.monthly_investment / self.monthly_income) * 100,

            1

        ) if self.monthly_income > 0 else 0

        if future_value >= total_invested * 2:

            goal_probability = "Very High"

        elif future_value >= total_invested * 1.5:

            goal_probability = "High"

        elif future_value >= total_invested:

            goal_probability = "Moderate"

        else:

            goal_probability = "Low"

        ai_advice = []

        if saving_rate < 20:

            ai_advice.append(
                "Increase your monthly savings to at least 20% of your income."
            )

        if self.annual_return < 10:

            ai_advice.append(
                "Consider investments with better long-term growth potential."
            )

        if self.years < 10:

            ai_advice.append(
                "A longer investment horizon generally improves compounding."
            )

        if not ai_advice:

            ai_advice.append(
                "Excellent! Your current financial plan is well balanced."
            )

        return {

            "monthly_income": round(self.monthly_income),

            "monthly_expense": round(self.monthly_expense),

            "monthly_investment": round(self.monthly_investment),

            "annual_return": self.annual_return,

            "salary_growth": self.salary_growth,

            "inflation": self.inflation,

            "years": self.years,

            "future_value": future_value,

            "total_invested": total_invested,

            "total_returns": total_returns,

            "net_worth": future_value,

            "inflation_adjusted_value": inflation_adjusted_value,

            "saving_rate": saving_rate,

            "goal_probability": goal_probability,

            "yearly_growth": yearly_growth,

            "ai_advice": ai_advice

        }