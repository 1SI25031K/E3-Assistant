import os
import sys
import logging
from flask import Flask, request, jsonify
from slack_sdk.signature import SignatureVerifier

# プロジェクトルートへのパス設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from backend.common.models import SlackMessage
# さっき改造した main.py の関数をインポート
from backend.main import run_pipeline

app = Flask(__name__)

# 1. 署名検証器の準備
# .env の SLACK_SIGNING_SECRET を使って、通信の改ざんがないかチェックする道具
verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    SlackからのWebhook (HTTP POST) を受け取るエンドポイント
    """
    # 2. 署名検証 (Security Check)
    # リクエストが正当なSlackからのものかを確認。偽装ならここで弾く。
    if not verifier.is_valid_request(request.get_data(), request.headers):
        return jsonify({"status": "invalid_request"}), 403

    data = request.json

    # 3. URL検証 (Challenge) 対応
    # Slackアプリの設定時に送られてくる「生存確認」パケットへの応答
    if "type" in data and data["type"] == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    # 4. イベント処理 (Event Callback)
    if "event" in data:
        event = data["event"]
        
        # ボット自身の発言は無視する (無限ループ防止)
        if "bot_id" in event:
            return jsonify({"status": "ignored_bot_message"})

        # ユーザーIDとテキストを抽出
        user_id = event.get("user")
        text = event.get("text")
        ts = event.get("ts")  # タイムスタンプをIDの一部に使う
        
        # メンションされた場合など、データ構造が少し変わる場合があるので安全に取得
        if not user_id or not text:
            return jsonify({"status": "ignored_no_content"})

        print(f"👂 [F-01] Message received from {user_id}: {text}")

        # 5. Contract A の作成 (正規化)
        # 雑多なJSONから、チーム共通の SlackMessage オブジェクトへ変換
        input_message = SlackMessage(
            event_id=f"evt_{ts}",    # 一意なID
            user_id=user_id,
            text_content=text,
            intent_tag="tbd",        # まだ判定していないので TBD (To Be Determined)
            status="pending"
        )

        # 6. パイプラインの起動 (F-02以降へパス)
        # Flaskの応答(200 OK)を素早く返すため、本来は非同期でやるべきだが
        # まずは直接呼び出しで実装する。
        try:
            run_pipeline(input_message)
        except Exception as e:
            print(f"❌ Pipeline Error: {e}")
            # エラー起きてもSlackには「受け取ったよ」と返すのが作法
    
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # ポート3000で起動
    print("🚀 Slacker Listener Server running on port 3000...")
    app.run(port=3000)
