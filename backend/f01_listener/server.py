import os
import sys
import threading
from dotenv import load_dotenv  # ★これを追加！

# プロジェクトルートへのパス設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

# ★これを追加！ (.envファイルから環境変数を読み込む)
load_dotenv()

import logging
from flask import Flask, request, jsonify
from slack_sdk.signature import SignatureVerifier
from backend.common.models import SlackMessage
from backend.main import run_pipeline

app = Flask(__name__)

# 環境変数が読み込まれているかチェック
if not os.environ.get("SLACK_SIGNING_SECRET"):
    print("❌ Error: SLACK_SIGNING_SECRET が見つかりません。.envを確認してください。")
    sys.exit(1)

# 署名検証器
verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    SlackからのWebhookを受け取る
    """
    # 1. 署名検証
    if not verifier.is_valid_request(request.get_data(), request.headers):
        return jsonify({"status": "invalid_request"}), 403

    data = request.json

    # 2. URL検証
    if "type" in data and data["type"] == "url_verification":
        return jsonify({"challenge": data["challenge"]})
    
    # 再送対策
    if request.headers.get("X-Slack-Retry-Num"):
        print("♻️ Ignoring Retry request from Slack")
        return jsonify({"status": "ignored_retry"})

    # 3. イベント処理
    if "event" in data:
        event = data["event"]
        
        if "bot_id" in event:
            return jsonify({"status": "ignored_bot_message"})

        user_id = event.get("user")
        text = event.get("text")
        ts = event.get("ts")
        channel_id = event.get("channel")

        if not user_id or not text:
            return jsonify({"status": "ignored_no_content"})

        print(f"👂 [F-01] Message received from {user_id}: {text}")

        # SlackMessage生成
        input_message = SlackMessage(
            event_id=f"evt_{ts}",
            user_id=user_id,
            channel_id=channel_id,
            text_content=text,
            intent_tag="tbd",
            status="pending"
        )

        # 4. パイプラインを別スレッドで起動
        x = threading.Thread(target=run_pipeline, args=(input_message,))
        x.start()
    
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("🚀 Slacker Listener Server running on port 3000...")
    app.run(port=3000)