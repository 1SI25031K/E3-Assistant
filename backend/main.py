import sys
import os
from dotenv import load_dotenv

# パス設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# 環境変数読み込み
load_dotenv()

from backend.common.models import SlackMessage, FeedbackResponse
from backend.f02_filter.filter import analyze_intent
# F-03: クラスベースのインポートに変更
from backend.f03_db.database import DynamoDBHandler 

try:
    from backend.f04_gen.generator import generate_feedback
except ImportError:
    from backend.f04_gen.generator import generate_feedback

from backend.f05_archive.logger import archive_process
from backend.f06_notify.notifier import send_reply


def run_pipeline(input_message: SlackMessage):
    """
    Slackerのメイン処理パイプライン（Phase 2: RAG統合版）
    """
    print(f"🟦 Pipeline Started for Event: {input_message.event_id}")
    
    # DBハンドラの初期化
    db = DynamoDBHandler()

    # --- Phase 1: Intent Analysis (F-02) ---
    analyzed_message = analyze_intent(input_message)
    print(f"🟨 判定結果: {analyzed_message.intent_tag}")
    
    # --- Phase 2: Save Initial Status (F-03) ---
    # analyzed_message に基づいてDBにログを保存
    db.save_log(analyzed_message)

    # フィルタリング（質問以外は無視）
    allow_list = ["question", "consultation"]
    if analyzed_message.intent_tag not in allow_list:
        print(f"☕ '{analyzed_message.intent_tag}' なので返信せずに終了します。")
        print(f"🟩 Pipeline Finished (Skipped Reply)\n")
        return

    # --- Phase 2.5: Context Retrieval (F-03拡張: RAG) ---
    # 【追加】生成の前に最新10件の履歴を取得する
    print(f"🔍 過去の文脈を取得中...")
    history_context = db.get_recent_history(input_message.channel_id, limit=10)

    # --- Phase 3: AI Generation (F-04) ---
    # 【修正】generate_feedback に history_context を渡す
    feedback_response = generate_feedback(analyzed_message, context=history_context)
    
    # --- Phase 4: Archive Result (F-05) ---
    # 生成された回答をDBに追記（save_logのfeedback引数を使用）
    db.save_log(analyzed_message, feedback=feedback_response)
    archive_process(feedback_response)

    # --- Phase 5: Notification (F-06) ---
    send_reply(feedback_response, input_message.channel_id)

    print(f"🏁 Pipeline Finished for Event: {input_message.event_id}")