import os
import sys
import threading
import logging
from dotenv import load_dotenv

# プロジェクトルートへのパス設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

# 環境変数の読み込み
load_dotenv()

from flask import Flask, request, jsonify
from slack_sdk.signature import SignatureVerifier

# Contract準拠
from backend.common.models import SlackMessage
from backend.main import run_pipeline

app = Flask(__name__)

# ---------------------------------------------------------
# 設定値のチェック
# ---------------------------------------------------------
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID")

if not SLACK_SIGNING_SECRET:
    print("❌ Error: SLACK_SIGNING_SECRET が見つかりません。")
    # Lambda環境では環境変数が設定されている前提のため、ローカル開発時のみexit
    if __name__ == "__main__":
        sys.exit(1)

if not TARGET_CHANNEL_ID:
    print("❌ Error: TARGET_CHANNEL_ID が見つかりません。.envに設定してください。")
    # 起動はさせますが、ログで警告します

# 署名検証器（SLACK_SIGNING_SECRETがない場合は後でエラーになる）
verifier = None
if SLACK_SIGNING_SECRET:
    verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    [F-01] Slack Event Listener (Active Monitoring Mode)
    指定チャンネルの全メッセージを監視し、フィルタリングしてパイプラインへ流す
    """
    # 1. 署名検証 (Security First)
    if not verifier:
        return jsonify({"status": "server_error", "message": "SLACK_SIGNING_SECRET not configured"}), 500
    
    if not verifier.is_valid_request(request.get_data(), request.headers):
        return jsonify({"status": "invalid_request"}), 403

    data = request.json

    # 2. URL検証 (Slack API仕様)
    if "type" in data and data["type"] == "url_verification":
        return jsonify({"challenge": data["challenge"]})
    
    # 再送対策 (ヘッダーチェック)
    if request.headers.get("X-Slack-Retry-Num"):
        # ログがうるさくなるのでprintはコメントアウトまたはdebugレベル推奨
        # print("♻️ Ignoring Retry request from Slack")
        return jsonify({"status": "ignored_retry"})

    # 3. イベント処理本体
    if "event" in data:
        event = data["event"]
        channel_id = event.get("channel")
        user_id = event.get("user")
        text = event.get("text", "")
        ts = event.get("ts")
        subtype = event.get("subtype")

        # --- 🛡️ フィルタリング・ロジック (Gatekeeper) ---

        # A. チャンネルチェック: 指定されたチャンネル以外は無視
        # (これをしないと、Botがいる全チャンネルで反応してしまいます)
        if channel_id != TARGET_CHANNEL_ID:
            return jsonify({"status": "ignored_other_channel"})

        # B. Botチェック: 自分自身や他のBotのメッセージは無視
        # subtypeが 'bot_message' の場合や、bot_idが存在する場合はスキップ
        if "bot_id" in event or subtype == "bot_message":
            return jsonify({"status": "ignored_bot_message"})
        
        # C. コンテンツチェック: テキストがないイベント（画像のアップロードのみ等）は一旦無視
        if not text:
            return jsonify({"status": "ignored_no_text"})

        # ------------------------------------------------

        print(f"👂 [F-01] Valid Message detected: {text[:30]}...")

        # 4. Contract A: SlackMessage生成
        # まだ質問かどうかわからないので、intent_tag="pending" で初期化
        input_message = SlackMessage(
            event_id=f"evt_{ts}",
            user_id=user_id,
            channel_id=channel_id,
            text_content=text,
            intent_tag="pending",  # F-02で判定されるため保留
            status="received"
        )

        # 5. パイプライン起動 (非同期)
        # サーバーは即座にSlackへ200 OKを返す必要があるため、処理は別スレッドへ
        process_thread = threading.Thread(target=run_pipeline, args=(input_message,))
        process_thread.start()
    
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print(f"🚀 Slacker Listener running on port 3000")
    print(f"👀 Watching Channel ID: {TARGET_CHANNEL_ID}")
    app.run(port=3000)