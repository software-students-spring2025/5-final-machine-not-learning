from flask import Blueprint, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_login import current_user

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

ai_bp = Blueprint("ai_suggest", __name__)

@ai_bp.route("/ask", methods=["POST"])
def ai_recommend():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    try:
        # ✅ 使用旧版 openai.ChatCompletion.create() 而不是 openai.OpenAI()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You're a creative mixologist bartender. Based on the user's mood or ingredients, recommend a unique cocktail idea with ingredients and how to make it."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300,
            temperature=0.9
        )

        result = response["choices"][0]["message"]["content"]
        return jsonify({
            "recommendation": result,
            "user_logged": current_user.is_authenticated
        })

    except Exception as e:
        print("❌ AI ERROR:", e)
        return jsonify({"error": str(e)}), 500
