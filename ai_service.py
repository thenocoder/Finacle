from collections import defaultdict
from statistics import mean

from flask_login import current_user

from models.transaction import Transaction
from models.ai_history import AIHistory
from extensions import db


class AIService:
    """
    Finacle AI Service

    Responsible for:

    • Financial Summary
    • Monthly Analytics
    • Category Analytics
    • Payment Analytics
    • Financial Health
    • AI Insights
    • AI Recommendations
    • Expense Prediction
    • AI History
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self, user_id=None):

        self.user_id = user_id or current_user.id

        self.transactions = (

            Transaction.query

            .filter_by(user_id=self.user_id)

            .order_by(Transaction.date.asc())

            .all()

        )

    # =====================================================
    # BASIC SUMMARY
    # =====================================================

    def total_income(self):

        return round(

            sum(

                transaction.amount

                for transaction in self.transactions

                if transaction.type.lower() == "income"

            ),

            2

        )

    def total_expense(self):

        return round(

            sum(

                transaction.amount

                for transaction in self.transactions

                if transaction.type.lower() == "expense"

            ),

            2

        )

    def net_balance(self):

        return round(

            self.total_income() -

            self.total_expense(),

            2

        )

    def savings_rate(self):

        income = self.total_income()

        if income == 0:
            return 0

        savings = income - self.total_expense()

        return round(

            (savings / income) * 100,

            2

        )

    # =====================================================
    # MONTHLY ANALYTICS
    # =====================================================

    def monthly_income(self):

        monthly = defaultdict(float)

        for transaction in self.transactions:

            if transaction.type.lower() == "income":

                key = transaction.date.strftime("%b %Y")

                monthly[key] += transaction.amount

        return dict(monthly)

    def monthly_expense(self):

        monthly = defaultdict(float)

        for transaction in self.transactions:

            if transaction.type.lower() == "expense":

                key = transaction.date.strftime("%b %Y")

                monthly[key] += transaction.amount

        return dict(monthly)

    def monthly_cashflow(self):

        income = self.monthly_income()

        expense = self.monthly_expense()

        months = sorted(

            set(income.keys())

            |

            set(expense.keys())

        )

        result = []

        for month in months:

            result.append({

                "month": month,

                "income": income.get(month, 0),

                "expense": expense.get(month, 0),

                "balance":

                    income.get(month, 0)

                    -

                    expense.get(month, 0)

            })

        return result

    # =====================================================
    # CATEGORY ANALYSIS
    # =====================================================

    def category_breakdown(self):

        categories = defaultdict(float)

        for transaction in self.transactions:

            if transaction.type.lower() == "expense":

                categories[transaction.category] += transaction.amount

        return dict(

            sorted(

                categories.items(),

                key=lambda item: item[1],

                reverse=True

            )

        )

    def top_category(self):

        categories = self.category_breakdown()

        if not categories:
            return None

        category = max(

            categories,

            key=categories.get

        )

        return {

            "category": category,

            "amount": round(

                categories[category],

                2

            )

        }

    # =====================================================
    # PAYMENT METHOD ANALYSIS
    # =====================================================

    def payment_method_analysis(self):

        methods = defaultdict(float)

        for transaction in self.transactions:

            if transaction.type.lower() == "expense":

                methods[transaction.payment_method] += transaction.amount

        return dict(

            sorted(

                methods.items(),

                key=lambda item: item[1],

                reverse=True

            )

        )

    # =====================================================
    # LARGEST EXPENSE
    # =====================================================

    def largest_expense(self):

        expenses = [

            transaction

            for transaction in self.transactions

            if transaction.type.lower() == "expense"

        ]

        if not expenses:
            return None

        largest = max(

            expenses,

            key=lambda transaction: transaction.amount

        )

        return {

            "title": largest.title,

            "category": largest.category,

            "amount": largest.amount,

            "date": largest.date

        }

    # =====================================================
    # AVERAGES
    # =====================================================

    def average_daily_spending(self):

        expenses = [

            transaction.amount

            for transaction in self.transactions

            if transaction.type.lower() == "expense"

        ]

        if not expenses:
            return 0

        unique_days = {

            transaction.date

            for transaction in self.transactions

            if transaction.type.lower() == "expense"

        }

        if len(unique_days) == 0:
            return 0

        return round(

            sum(expenses) / len(unique_days),

            2

        )

    def average_transaction(self):

        if not self.transactions:
            return 0

        return round(

            mean(

                transaction.amount

                for transaction in self.transactions

            ),

            2

        )
          # =====================================================
    # FINANCIAL HEALTH SCORE
    # =====================================================

    def financial_health_score(self):

        score = 100

        income = self.total_income()
        expense = self.total_expense()
        savings_rate = self.savings_rate()

        if income <= 0:

            return {
                "score": 0,
                "status": "No Income",
                "color": "danger"
            }

        # Savings Rate

        if savings_rate >= 40:
            score += 0

        elif savings_rate >= 25:
            score -= 5

        elif savings_rate >= 15:
            score -= 15

        elif savings_rate >= 10:
            score -= 25

        else:
            score -= 40

        # Expense Ratio

        expense_ratio = (expense / income) * 100

        if expense_ratio > 90:
            score -= 20

        elif expense_ratio > 80:
            score -= 10

        # Category Count

        if len(self.category_breakdown()) > 10:
            score -= 10

        # Large Expense

        largest = self.largest_expense()

        if largest:

            if largest["amount"] > income * 0.30:
                score -= 10

        score = max(0, min(100, int(score)))

        if score >= 85:

            status = "Excellent"
            color = "success"

        elif score >= 70:

            status = "Good"
            color = "primary"

        elif score >= 50:

            status = "Average"
            color = "warning"

        else:

            status = "Needs Improvement"
            color = "danger"

        return {

            "score": score,
            "status": status,
            "color": color

        }

    # =====================================================
    # SMART INSIGHTS
    # =====================================================

    def smart_insights(self):

        insights = []

        income = self.total_income()
        expense = self.total_expense()

        if income == 0:

            insights.append(
                "No income has been recorded yet. Add your income to receive accurate financial analysis."
            )

            return insights

        savings_rate = self.savings_rate()

        if savings_rate >= 30:

            insights.append(
                f"Excellent! You are saving {savings_rate}% of your income."
            )

        elif savings_rate >= 20:

            insights.append(
                f"You are maintaining a healthy savings rate of {savings_rate}%."
            )

        else:

            insights.append(
                f"Your savings rate is only {savings_rate}%. Try saving at least 20%."
            )

        top = self.top_category()

        if top:

            insights.append(
                f"Your highest spending category is '{top['category']}' with total spending of ₹{top['amount']:,.2f}."
            )

        payment = self.payment_method_analysis()

        if payment:

            method = max(payment, key=payment.get)

            insights.append(
                f"Most of your expenses are paid using {method}."
            )

        largest = self.largest_expense()

        if largest:

            insights.append(
                f"Your largest expense was '{largest['title']}' worth ₹{largest['amount']:,.2f}."
            )

        return insights

    # =====================================================
    # AI RECOMMENDATIONS
    # =====================================================

    def recommendations(self):

        recommendations = []

        income = self.total_income()
        expense = self.total_expense()

        if income == 0:

            recommendations.append(
                "Start recording your income to unlock personalized recommendations."
            )

            return recommendations

        savings_rate = self.savings_rate()

        if savings_rate < 20:

            recommendations.append(
                "Aim to save at least 20% of your monthly income."
            )

        categories = self.category_breakdown()

        if categories:

            highest = max(categories, key=categories.get)

            amount = categories[highest]

            if amount > expense * 0.30:

                recommendations.append(
                    f"Reduce spending in '{highest}' because it contributes a large portion of your expenses."
                )

        methods = self.payment_method_analysis()

        if methods:

            upi = methods.get("UPI", 0)

            if expense > 0 and upi > (expense * 0.60):

                recommendations.append(
                    "A large percentage of your expenses are through UPI. Monitor impulse purchases carefully."
                )

        if expense > income:

            recommendations.append(
                "Your expenses currently exceed your income. Reduce discretionary spending immediately."
            )

        if not recommendations:

            recommendations.append(
                "Your financial habits look healthy. Continue maintaining your current budgeting strategy."
            )

        return recommendations

    # =====================================================
    # EXPENSE PREDICTION
    # =====================================================

    def predict_next_month_expense(self):

        monthly = self.monthly_expense()

        values = list(monthly.values())

        if not values:
            return 0

        if len(values) == 1:
            return round(values[0], 2)

        if len(values) == 2:
            return round(sum(values) / 2, 2)

        last_three = values[-3:]

        return round(
            sum(last_three) / len(last_three),
            2
        )

    # =====================================================
    # MONTHLY TREND
    # =====================================================

    def monthly_trend(self):

        values = list(self.monthly_expense().values())

        if len(values) < 2:

            return {

                "trend": "Stable",

                "percentage": 0

            }

        previous = values[-2]
        current = values[-1]

        if previous == 0:
            percent = 100

        else:

            percent = round(
                ((current - previous) / previous) * 100,
                2
            )

        if percent > 5:
            trend = "Increasing"

        elif percent < -5:
            trend = "Decreasing"

        else:
            trend = "Stable"

        return {

            "trend": trend,

            "percentage": percent

        }
            # =====================================================
    # SAVE AI HISTORY
    # =====================================================

    def save_ai_history(
        self,
        analysis_type,
        prompt,
        response
    ):

        history = AIHistory(

            user_id=self.user_id,

            analysis_type=analysis_type,

            prompt=prompt,

            response=response

        )

        db.session.add(history)

        db.session.commit()

        return history

    # =====================================================
    # GET AI HISTORY
    # =====================================================

    def get_history(self, limit=20):

        return (

            AIHistory.query

            .filter_by(
                user_id=self.user_id
            )

            .order_by(
                AIHistory.created_at.desc()
            )

            .limit(limit)

            .all()

        )

    # =====================================================
    # COMPLETE DASHBOARD DATA
    # =====================================================

    def get_dashboard_data(self):

        health = self.financial_health_score()

        top_category = self.top_category()

        largest_expense = self.largest_expense()

        prediction = self.predict_next_month_expense()

        return {

            # -------------------------------------------------
            # Summary
            # -------------------------------------------------

            "summary": {

                "income": self.total_income(),

                "expense": self.total_expense(),

                "balance": self.net_balance(),

                "savings_rate": self.savings_rate(),

                "health_score": health["score"],

                "health_status": health["status"],

                "health_color": health["color"],

                "top_category":

                    top_category["category"]

                    if top_category else None,

                "top_category_amount":

                    top_category["amount"]

                    if top_category else 0,

                "largest_expense":

                    largest_expense["title"]

                    if largest_expense else None,

                "largest_expense_amount":

                    largest_expense["amount"]

                    if largest_expense else 0

            },

            # -------------------------------------------------
            # Health
            # -------------------------------------------------

            "health": health,

            # -------------------------------------------------
            # Prediction
            # -------------------------------------------------

            "prediction": {

                "predicted_expense": prediction

            },

            # -------------------------------------------------
            # Charts
            # -------------------------------------------------

            "monthly_income":

                self.monthly_income(),

            "monthly_expense":

                self.monthly_expense(),

            "cashflow":

                self.monthly_cashflow(),

            "category_breakdown":

                self.category_breakdown(),

            "payment_methods":

                self.payment_method_analysis(),

            # -------------------------------------------------
            # Statistics
            # -------------------------------------------------

            "average_daily_spending":

                self.average_daily_spending(),

            "average_transaction":

                self.average_transaction(),

            "top_category":

                top_category,

            "largest_expense":

                largest_expense,

            "trend":

                self.monthly_trend(),

            # -------------------------------------------------
            # AI
            # -------------------------------------------------

            "insights":

                self.smart_insights(),

            "recommendations":

                self.recommendations(),
                "recommendation": self.recommendations()[0],

            # -------------------------------------------------
            # History
            # -------------------------------------------------

                        # -------------------------------------------------
            # History
            # -------------------------------------------------

            "history": [
                {
                    "id": item.id,
                    "prompt": item.prompt,
                    "response": item.response,
                    "analysis_type": item.analysis_type,
                    "created_at": item.created_at.strftime("%d %b %Y %I:%M %p")
                }
                for item in self.get_history()
            ]

        }