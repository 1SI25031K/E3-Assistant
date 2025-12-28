import sys
import os
from typing import Optional

# パス設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from backend.common.models import SlackMessage, FeedbackResponse
# 各モジュールの機能をインポート
# ※ファイルがない等のエラーが出る場合は、適宜コメントアウト対応してください
try:
    from backend.f02_filter.filter import analyze_intent       # F-02
    from backend.f03_db.database import save_to_db             # F-03
    from backend.f04_gen.generater import generate_feedback    # F-04
    from backend.f05_archive.logger import archive_process     # F-05
    from backend.f06_notify.notifier import send_reply         # F-06
except ImportError:
    pass

def run_pipeline(input_message: SlackMessage):
    """
    Slackerのメイン処理パイプライン
    """
    print(f"\n🚀 Pipeline Started for Event: {input_message.event_id}")

    # --- Phase 1: Intent Analysis (F-02) ---
    # ここで「chat(雑談)」か「question(質問)」かを判定しています
    analyzed_message = analyze_intent(input_message)
    print(f"🧐 判定結果: {analyzed_message.intent_tag}")
    
    # --- Phase 2: Save Initial Status (F-03) ---
    # 記録だけは残しておきます
    save_to_db(analyzed_message)

    # ▼▼▼【ここが今回の修正ポイント！】▼▼▼
    # 判定結果が「質問(question)」や「相談(consultation)」以外なら、ここで帰ります。
    # ※ F-02が返すタグ名に合わせて調整してください（ログを見る限り 'question' です）
    allow_list = ["question", "consultation"]
    
    if analyzed_message.intent_tag not in allow_list:
        print(f"☕ '{analyzed_message.intent_tag}' なので返信せずに終了します。")
        print(f"🏁 Pipeline Finished (Skipped Reply)\n")
        return
    # ▲▲▲ --------------------------------

    # --- Phase 3: AI Generation (F-04) ---
    feedback_response = generate_feedback(analyzed_message)
    
    # --- Phase 4: Archive Result (F-05) ---
    archive_process(feedback_response)

    # --- Phase 5: Notification (F-06) ---
    # 質問のときだけ、ここまで到達して返信されます
    send_reply(feedback_response, input_message.channel_id)

    print(f"🏁 Pipeline Finished for Event: {input_message.event_id}\n")