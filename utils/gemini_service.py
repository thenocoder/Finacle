import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()


class GeminiService:
    """
    Handles all communication with Google Gemini AI.
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables."
            )

        genai.configure(api_key=api_key)

        # Use a currently supported Gemini model.
        self.model = genai.GenerativeModel(
            model_name="models/gemini-3.6-flash"
        )

    # ==========================================================
    # Build Prompt
    # ==========================================================

    def build_prompt(
        self,
        dashboard_data,
        user_question
    ):

        summary = dashboard_data.get("summary", {})
        prediction = dashboard_data.get("prediction", {})
        insights = dashboard_data.get("insights", [])
        recommendations = dashboard_data.get("recommendations", [])

        prompt = f"""
You are Finacle AI.

You are an intelligent personal financial advisor.

Always answer professionally.

Never mention that you are Gemini or a Google AI model.

Give practical and personalized financial advice.

====================================================

USER FINANCIAL SUMMARY

Total Income:
₹ {summary.get("income", 0):,.2f}

Total Expense:
₹ {summary.get("expense", 0):,.2f}

Current Balance:
₹ {summary.get("balance", 0):,.2f}

Savings Rate:
{summary.get("savings_rate", 0)}%

Financial Health Score:
{summary.get("health_score", 0)}/100

Top Spending Category:
{summary.get("top_category", "N/A")}

Largest Expense:
{summary.get("largest_expense", "N/A")}
₹ {summary.get("largest_expense_amount", 0):,.2f}

====================================================

NEXT MONTH PREDICTION

Predicted Expense:
₹ {prediction.get("predicted_expense", 0):,.2f}

====================================================

AI INSIGHTS

{chr(10).join("- " + str(item) for item in insights)}

====================================================

CURRENT RECOMMENDATIONS

{chr(10).join("- " + str(item) for item in recommendations)}

====================================================

USER QUESTION

{user_question}

====================================================

INSTRUCTIONS

1. Personalize your answer using the user's financial data.
2. Keep answers practical.
3. Use Markdown.
4. Use headings.
5. Use bullet points.
6. Mention actual financial values whenever useful.
7. Give one actionable recommendation at the end.
8. Keep the response under 300 words unless detailed analysis is requested.
"""

        return prompt

    # ==========================================================
    # Generate AI Response
    # ==========================================================

    def generate_response(
        self,
        dashboard_data,
        user_question
    ):

        try:

            prompt = self.build_prompt(
                dashboard_data,
                user_question
            )

            response = self.model.generate_content(prompt)

            if (
                hasattr(response, "text")
                and response.text
            ):
                return response.text.strip()

            # Fallback parsing for responses without .text
            if (
                hasattr(response, "candidates")
                and response.candidates
            ):

                parts = (
                    response.candidates[0]
                    .content.parts
                )

                text = ""

                for part in parts:

                    if hasattr(part, "text"):
                        text += part.text

                if text.strip():
                    return text.strip()

            return (
                "Sorry, I couldn't generate a response at the moment."
            )

        except Exception as e:

            return (
                f"⚠️ Gemini Error:\n\n{str(e)}"
            )

    # ==========================================================
    # Health Check
    # ==========================================================

    def test_connection(self):

        try:

            response = self.model.generate_content(
                "Reply only with: Connection Successful"
            )

            text = ""

            if hasattr(response, "text"):
                text = response.text.strip()

            return {
                "success": True,
                "message": text or "Connection Successful"
            }

        except Exception as e:

            return {
                "success": False,
                "message": str(e)
            }

    # ==========================================================
    # Available Models (Debug Helper)
    # ==========================================================

    @staticmethod
    def list_available_models():

        try:

            models = []

            for model in genai.list_models():

                if "generateContent" in model.supported_generation_methods:
                    models.append(model.name)

            return models

        except Exception as e:

            return [str(e)]
