from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from models.ai_history import AIHistory
from services.ai_service import AIService
from utils.gemini_service import GeminiService

from extensions import db


ai_bp = Blueprint(
    "ai",
    __name__,
    url_prefix="/ai"
)


# ==========================================================
# AI Assistant Page
# ==========================================================

@ai_bp.route("/")
@login_required
def assistant():

    ai_service = AIService(current_user.id)

    dashboard_data = ai_service.get_dashboard_data()

    history = (
        AIHistory.query
        .filter_by(user_id=current_user.id)
        .order_by(AIHistory.created_at.desc())
        .limit(20)
        .all()
    )

    return render_template(

        "ai/assistant.html",

        ai=dashboard_data,

        history=history

    )


# ==========================================================
# Chat Endpoint
# ==========================================================

@ai_bp.route("/chat", methods=["POST"])
@login_required
def chat():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No request received."
        }), 400

    question = data.get("message", "").strip()

    if question == "":

        return jsonify({
            "success": False,
            "message": "Message cannot be empty."
        }), 400

    try:

        ai_service = AIService(current_user.id)

        dashboard_data = ai_service.get_dashboard_data()

        gemini = GeminiService()

        response = gemini.generate_response(

            dashboard_data,

            question

        )

        history = AIHistory(

            user_id=current_user.id,

            analysis_type="Chat",

            prompt=question,

            response=response

        )

        db.session.add(history)

        db.session.commit()

        return jsonify({

            "success": True,

            "response": response

        })
    except Exception as e:
         import traceback

   

    traceback.print_exc()

    return jsonify({

        "success": False,

        "message": str(e)

    }), 500

    


# ==========================================================
# Dashboard Data API
# ==========================================================

@ai_bp.route("/dashboard")
@login_required
def dashboard_data():

    ai_service = AIService(current_user.id)

    return jsonify(

        ai_service.get_dashboard_data()

    )


# ==========================================================
# Chat History
# ==========================================================

@ai_bp.route("/history")
@login_required
def history():

    chats = (

        AIHistory.query

        .filter_by(

            user_id=current_user.id

        )

        .order_by(

            AIHistory.created_at.desc()

        )

        .all()

    )

    history_data = []

    for chat in chats:

        history_data.append({

            "id": chat.id,

            "prompt": chat.prompt,

            "response": chat.response,

            "analysis_type": chat.analysis_type,

            "created_at": chat.created_at.strftime(

                "%d %b %Y %I:%M %p"

            )

        })

    return jsonify({

        "success": True,

        "history": history_data

    })


# ==========================================================
# Clear Chat History
# ==========================================================

@ai_bp.route("/clear-history", methods=["POST"])
@login_required
def clear_history():

    AIHistory.query.filter_by(

        user_id=current_user.id

    ).delete()

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "Chat history cleared."

    })


# ==========================================================
# Test Gemini Connection
# ==========================================================

@ai_bp.route("/test")
@login_required
def test():

    gemini = GeminiService()

    return jsonify(

        gemini.test_connection()

    )
