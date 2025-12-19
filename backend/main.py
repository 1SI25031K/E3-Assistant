
import sys
import os
from dotenv import load_dotenv

# パス設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.common.models import SlackMessage
from backend.f03_db.database import save_to_db
from backend.f04_gen.generater import generate_feedback
from backend.f05_archive.logger import archive_process

load_dotenv()

def run_pipeline(input_message: SlackMessage):
    """
    外部(F-01)からSlackMessageを受け取り、
    F-03 -> F-04 -> F-05 のパイプラインを実行する指揮者関数。
    """
    print(f"🚀Pipeline Triggered for Event: {input_message.event_id}")

    # [Step 1] Initial Save (F-03)
    # まず「受信しました」という記録を残す
    if not save_to_db(input_message):
        print("❌ Pipeline Aborted: Failed to save initial data.")
        return

    # [Step 2] Generate Answer (F-04)
    # AIに回答を作らせる
    print(f"⚙️ Calling F-04...")
    feedback_response = generate_feedback(input_message)
    
    # [Step 3] Archive & Notify (F-05/F-06)
    # 結果を保存し、完了とする
    # ※本来の設計では F-06(Notify) は F-05 の後、または F-05 内で呼ばれるべきですが
    #   今回は F-05 が DB更新を担当しているため、通知処理(F-06)もここに追加します。
    #   (今回はシンプルに F-05 内で完結、またはここで F-06 を呼ぶ形にします)
    
    print(f"💾 Calling F-05...")
    archive_process(feedback_response)

    # ★追加: F-06 (Notify) を呼び出す
    # F-06 はまだ main.py にインポートしていませんが、
    # 完了後に通知を送る処理が必要です。
    from backend.f06_notify.notifier import send_reply
    print(f"📤 Calling F-06...")
    send_reply(feedback_response)

    print("🏁 Pipeline Finished.")

# 開発用: このファイルを直接実行した時だけダミーデータで動く
if __name__ == "__main__":
    dummy_msg = SlackMessage(
        event_id="MANUAL_TEST_001",
        user_id="U_ME",
        text_content="手動テストです",
        intent_tag="test",
        status="pending"
    )
    run_pipeline(dummy_msg)