from collections import defaultdict
from statistics import mean


class ExpensePredictor:

    def __init__(self, transactions):

        self.transactions = transactions

    # ======================================================
    # Predict Next Month Expense
    # ======================================================

    def predict(self):

        monthly_data = defaultdict(float)

        for transaction in self.transactions:

            if transaction.type != "Expense":
                continue

            key = (
                transaction.date.year,
                transaction.date.month
            )

            monthly_data[key] += float(transaction.amount)

        history = list(monthly_data.values())

        if not history:

            return {
                "prediction": 0,
                "average": 0,
                "highest": 0,
                "lowest": 0,
                "trend": "No Data"
            }

        average = mean(history)

        highest = max(history)

        lowest = min(history)

        # --------------------------------------
        # Trend
        # --------------------------------------

        if len(history) >= 2:

            last = history[-1]
            previous = history[-2]

            if last > previous:

                trend = "Increasing"

            elif last < previous:

                trend = "Decreasing"

            else:

                trend = "Stable"

        else:

            trend = "Stable"

        # --------------------------------------
        # Prediction
        # --------------------------------------

        if trend == "Increasing":

            prediction = average * 1.10

        elif trend == "Decreasing":

            prediction = average * 0.95

        else:

            prediction = average

        return {

            "prediction": round(prediction, 2),

            "average": round(average, 2),

            "highest": round(highest, 2),

            "lowest": round(lowest, 2),

            "trend": trend

        }