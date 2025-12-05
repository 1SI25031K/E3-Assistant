import sys
import json
import os
import datetime

# 各モジュールのパスを通す
# これにより backend フォルダ内の f01... などを import できるようになります
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    print("🚀 === Emysys Pipeline Start (Phase 1) === 🚀")

    # --- 0. モジュールの読み込み ---
    try:
        from f01_listener.main import mock_receive_slack_message
        from f02_filter.main import process_data as f02_process
        from f04_generator.main import generate_feedback as f04_process
        from f05_archive.main import archive_process as f05_process
        print("✅ 全モジュールの読み込みに成功しました")
    except ImportError as e:
        print(f"⚠️ まだ実装されていない、またはパスが間違っているモジュールがあります: {e}")
        print("👉 メンバーが git push して、それをあなたが git pull するまでここは動きません。")
        sys.exit(1)

    # --- 1. F-01 Listener (ユウリ) ---
    print("\n[Step 1] Calling F-01 (Listener)...")
    json_from_f01 = mock_receive_slack_message()

    # 安全策: もしF-01がNoneを返した場合（return忘れ等）のダミーデータ
    if not json_from_f01:
        print("⚠️ Warning: F-01 returned None. Using dummy data for testing.")
        initial_data = {
            "source": "slack",
            "event_id": "evt_fallback_001",
            "user_id": "U_FALLBACK",
            "timestamp": datetime.datetime.now().isoformat(),
            "text_content": "テスト用メッセージ：明日のMTG資料はどこ？"
        }
        json_from_f01 = json.dumps(initial_data, ensure_ascii=False)
    
    print(f"   -> Data: {json_from_f01}")

    # --- 2. F-02 Filter (コウタ) ---
    print("\n[Step 2] Passing to F-02 (Filter)...")
    json_from_f02 = f02_process(json_from_f01)

    # 安全策: コウタさんが return を忘れているとここで None になり、次でエラーになるのを防ぐ
    if not json_from_f02:
        print("❌ Error: F-02 returned None. Pipeline stopped.")
        print("👉 コウタさんに「main.pyの最後で return json_str してください」と伝えてください。")
        return

    # --- 3. F-04 Generator (コウセイ) ---
    print("\n[Step 3] Passing to F-04 (Generator)...")
    json_from_f04 = f04_process(json_from_f02)
    
    if not json_from_f04:
        print("❌ Error: F-04 returned None. Pipeline stopped.")
        return

    # --- 4. F-05 Archive (コウセイ) ---
    print("\n[Step 4] Passing to F-05 (Archive)...")
    f05_process(json_from_f04)

    print("\n🏁 === Pipeline Finished Successfully ===")

if __name__ == "__main__":
    main()