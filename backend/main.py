import sys
import os
from dotenv import load_dotenv

# パス設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# 環境変数読み込み
load_dotenv()

from backend.common.models import SlackMessage, FeedbackResponse

# ▼▼▼【修正】エラー隠しをやめ、正しくインポートします ▼▼▼
# もしここでエラーが出る場合、ファイル名やフォルダ構成が間違っています
from backend.f02_filter.filter import analyze_intent       # F-02
from backend.f03_db.database import save_to_db             # F-03

# 【注意】ファイル名が generator.py か generater.py か確認してください
# リポジトリ通りなら generator ですが、もしエラーが出るなら generater に直してください
try:
    from backend.f04_gen.generator import generate_feedback # F-04
except ImportError:
    from backend.f04_gen.generater import generate_feedback # 綴り間違い対策

from backend.f05_archive.logger import archive_process     # F-05
from backend.f06_notify.notifier import send_reply         # F-06
# ▲▲▲ ------------------------------------------------

def run_pipeline(input_message: SlackMessage):
    """
    Slackerのメイン処理パイプライン
    """
    print(f"\n🚀 Pipeline Started for Event: {input_message.event_id}")

    # --- Phase 1: Intent Analysis (F-02) ---
    analyzed_message = analyze_intent(input_message)
    print(f"🧐 判定結果: {analyzed_message.intent_tag}")
    
    # --- Phase 2: Save Initial Status (F-03) ---
    save_to_db(analyzed_message)

    # フィルタリング（質問以外は無視）
    allow_list = ["question", "consultation"]
    if analyzed_message.intent_tag not in allow_list:
        print(f"☕ '{analyzed_message.intent_tag}' なので返信せずに終了します。")
        print(f"🏁 Pipeline Finished (Skipped Reply)\n")
        return

    # --- Phase 3: AI Generation (F-04) ---
    feedback_response = generate_feedback(analyzed_message)
    
    # --- Phase 4: Archive Result (F-05) ---
    archive_process(feedback_response)

    # --- Phase 5: Notification (F-06) ---
    send_reply(feedback_response, input_message.channel_id)

    print(f"🏁 Pipeline Finished for Event: {input_message.event_id}\n")