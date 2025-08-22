# main.py  (AstrBot OpenAI 适配版)
import os, json
from flask import Flask, request, jsonify
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_KEY"])
app = Flask(__name__)

sys_prompt = "你是一只傲娇猫娘，每句话最后都带个「喵～」"
model_name = "gemini-2.5-flash-latest"

@app.route("/v1/chat/completions", methods=["POST"])
def chat():
    data = request.get_json()
    messages = [{"role": "system", "content": sys_prompt}]
    messages += data.get("messages", [])
    try:
        resp = genai.GenerativeModel(model_name).generate_content(
            [f"{m['role']}: {m['content']}" for m in messages]
        )
        reply = resp.text
    except Exception as e:
        reply = f"出错啦：{e}"
    return jsonify({
        "choices": [{
            "message": {"role": "assistant", "content": reply},
            "finish_reason": "stop",
            "index": 0
        }],
        "model": "gemini-2.5-flash",
        "object": "chat.completion",
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
