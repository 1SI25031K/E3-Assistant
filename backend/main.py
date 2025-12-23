import sys
import os
from typing import Optional

# パス設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from backend.common.models import SlackMessage, FeedbackResponse
# 各モジュールの機能をインポート
from backend.f02_filter.filter import analyze_intent       # F-02
from backend.f03_db.database import save_to_db             # F-03
from backend.f04_gen.generater import generate_feedback    # F-04
from backend.f05_archive.logger import archive_process     # F-05
from backend.f06_notify.notifier import send_reply         # F-06

def run_pipeline(input_message: SlackMessage):
    """
    Slackerのメイン処理パイプライン
    F-01から受け取ったメッセージを順次加工し、最終的にSlackへ返す。
    """
    print(f"\n🚀 Pipeline Started for Event: {input_message.event_id}")

    # --- Phase 1: Intent Analysis (F-02) ---
    # ユーザーの意図を判定し、タグ付けする
    analyzed_message = analyze_intent(input_message)
    
    # --- Phase 2: Save Initial Status (F-03) ---
    # 「受信しました」という記録をDBに残す
    if not save_to_db(analyzed_message):
        print("⚠️ DB Save Failed (Phase 2), but continuing...")

    # --- Phase 3: AI Generation (F-04) ---
    # Geminiを使って回答を生成する (Contract B -> Contract C)
    feedback_response = generate_feedback(analyzed_message)
    
    # エラー時のガード: 生成に失敗していたらここで止める等の判断も可能だが、
    # 今回はFeedbackResponseにエラーメッセージが入っているのでそのまま進む

    # --- Phase 4: Archive Result (F-05) ---
    # 最終的な回答データをDBに保存する（F-03の機能を再利用）
    # ※ logger.py 経由で呼び出す
    archive_process(feedback_response)

    # --- Phase 5: Notification (F-06) ---
    # Slackに回答を送信する
    send_reply(feedback_response)

    print(f"🏁 Pipeline Finished for Event: {input_message.event_id}\n")

# 🧪 単体テスト用
if __name__ == "__main__":
    # テストデータ
    dummy_msg = SlackMessage(
        event_id="TEST_MAIN_001",
        user_id="U_TEST_ADMIN",
        text_content="パイプラインの結合テストです。",
        intent_tag="tbd",
        status="pending"
    )
    run_pipeline(dummy_msg)