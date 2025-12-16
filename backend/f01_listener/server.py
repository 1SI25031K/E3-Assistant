# backend/f01_listener/server.py (コウセイさんの実験用)
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Slackが「このURL生きてる？」と確認してくる処理 (Challenge認証)
@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    
    # 1. Slackからの接続確認 (Challenge) 対応
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})
    
    # 2. イベント受信 (ここが本番)
    if "event" in data:
        event = data["event"]
        # ボット自身の発言は無視する (無限ループ防止)
        if event.get("bot_id"):
            return jsonify({"status": "ignored"})
            
        print(f"📩 メッセージ受信: {event.get('text')}")
        
        # ここで本来は F-02 -> F-04 -> F-06 とバケツリレーを開始する
        
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # ポート3000でサーバーを起動
    print("🚀 Webhook Server Listening on port 3000...")
    app.run(port=3000, debug=True)