from typing import Dict


class AllocationEngine:

    def __init__(

        self,

        monthly_income,

        monthly_expense,

        profile

    ):

        self.income = float(monthly_income or 0)

        self.expense = float(monthly_expense or 0)

        self.profile = profile


    # ===============================================

    def generate(self) -> Dict:

        savings = max(

            self.income - self.expense,

            0

        )

        allocation = {

            "Emergency Fund": 0,

            "SIP": 0,

            "Stocks": 0,

            "Gold": 0,

            "PPF": 0,

            "FD": 0,

            "Cash Reserve": 0

        }

        advice = []

        if savings <= 0:

            advice.append(

                "Your monthly expenses exceed your income."

            )

            advice.append(

                "Reduce expenses before investing."

            )

            return {

                "income": self.income,

                "expense": self.expense,

                "available_savings": 0,

                "allocation": allocation,

                "advice": advice

            }

        # ============================================
        # Emergency Fund
        # ============================================

        if not self.profile.emergency_fund_available:

            emergency_percentage = 0.40

            advice.append(

                "Build your emergency fund first."

            )

        else:

            emergency_percentage = 0.10

        emergency = savings * emergency_percentage

        allocation["Emergency Fund"] = round(emergency)

        investable = savings - emergency

        # ============================================
        # Risk Based Allocation
        # ============================================

        risk = self.profile.risk_appetite

        if risk == "Low":

            sip = 0.20

            stock = 0.00

            gold = 0.20

            ppf = 0.35

            fd = 0.20

            cash = 0.05

        elif risk == "Medium":

            sip = 0.45

            stock = 0.15

            gold = 0.10

            ppf = 0.15

            fd = 0.05

            cash = 0.10

        else:

            sip = 0.30

            stock = 0.45

            gold = 0.05

            ppf = 0.05

            fd = 0.00

            cash = 0.15

        # ============================================
        # Investment Horizon
        # ============================================

        horizon = self.profile.investment_horizon

        if horizon == "1-3 Years":

            fd += 0.10

            stock -= 0.10

            advice.append(

                "Short investment horizon detected."

            )

        elif horizon == "5+ Years":

            stock += 0.05

            fd -= 0.05

            advice.append(

                "Long investment horizon allows greater equity exposure."

            )

        # ============================================
        # Goal Based Logic
        # ============================================

        goal = self.profile.financial_goal

        if goal == "Retirement":

            sip += 0.10

            ppf += 0.05

            advice.append(

                "Retirement planning focuses on long-term growth."

            )

        elif goal == "Emergency Fund":

            allocation["Emergency Fund"] += round(

                investable * 0.20

            )

            investable *= 0.80

            advice.append(

                "Priority given to emergency savings."

            )

        elif goal == "House Purchase":

            fd += 0.05

            cash += 0.05

            advice.append(

                "Maintaining liquidity for your future home."

            )

        elif goal == "Wealth Creation":

            stock += 0.05

            sip += 0.05

            advice.append(

                "Growth-oriented investment strategy selected."

            )

        # ============================================
        # Allocate
        # ============================================

        allocation["SIP"] = round(investable * sip)

        allocation["Stocks"] = round(investable * stock)

        allocation["Gold"] = round(investable * gold)

        allocation["PPF"] = round(investable * ppf)

        allocation["FD"] = round(investable * fd)

        allocation["Cash Reserve"] = round(investable * cash)

        # ============================================
        # Existing Investments
        # ============================================

        if self.profile.sip:

            advice.append(

                "Existing SIP detected."

            )

        if self.profile.stocks:

            advice.append(

                "Existing stock investments detected."

            )

        if self.profile.gold:

            advice.append(

                "Gold investment already exists."

            )

        if self.profile.ppf:

            advice.append(

                "PPF account already exists."

            )

        if self.profile.fd:

            advice.append(

                "Fixed Deposit already exists."

            )

        # ============================================
        # Savings Behaviour
        # ============================================

        saving_rate = (

            savings / self.income

        ) * 100

        if saving_rate < 20:

            advice.append(

                "Try saving at least 20% of your monthly income."

            )

        elif saving_rate >= 40:

            advice.append(

                "Excellent savings habit."

            )

        # ============================================

        return {

            "income": round(self.income),

            "expense": round(self.expense),

            "available_savings": round(savings),

            "saving_rate": round(saving_rate, 1),

            "allocation": allocation,

            "advice": advice

        }