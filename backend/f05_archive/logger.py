# backend/f05_archive/main.py
from backend.common.models import FeedbackResponse
from backend.f03_db.database import save_to_db

def archive_process(response: FeedbackResponse) -> bool:
    """
    [F-05] アーカイブ処理 (DynamoDBへの最終ステータス記録)
    
    F-04(Generator)から受け取った回答データ(FeedbackResponse)を、
    F-03(Database)の機能を使って永続化する。
    
    Args:
        response (FeedbackResponse): AI生成結果を含んだ完了データ
        
    Returns:
        bool: アーカイブ(DB更新)が成功すればTrue
    """
    print(f"--- 💾 [F-05] Archiving Process Start: {response.event_id} ---")
    
    # 1. DB更新処理を呼び出す (F-03へ委譲)
    # 自分で保存処理を書くのではなく、database.py の update_feedback を使う
    success = save_to_db(response)
    
    if success:
        print(f"✅ Archive Complete: Event {response.event_id} is now closed.")
        return True
    else:
        print(f"❌ Archive Failed: Could not update DB for {response.event_id}")
        return False

# 🧪 単体テスト用ブロック
if __name__ == "__main__":
    # テスト用のダミー完了データを作成
    test_response = FeedbackResponse(
        event_id="TEST_ARCHIVE_001",
        target_user_id="U_TEST_ARCHIVER",
        feedback_summary="【F-05テスト】アーカイブ機能の正常性を確認しました。",
        status="complete"
    )
    
    # ※注意: 単体テストでこれを成功させるには、
    # 先にDynamoDB上に "TEST_ARCHIVE_001" というIDを持つデータが存在している必要があります。
    # (update_itemは既存データがないと更新できない場合があるため)
    
    # 実行
    archive_process(test_response)