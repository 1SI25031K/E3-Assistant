
import sys
import os
import json

# パスを通すおまじない
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from f04_generator.main import generate_feedback
from f05_archive.main import archive_process

def main():
    print(" === Slacker F-04/05 Standalone Test Start === ")

    # 1. 【重要】Contract B のダミーデータ (コウタさんから渡ってくるはずのデータ)
    # 画像の仕様通りにここで定義する。「他人の完成」を待たずにここを変えればテストし放題。
    mock_input_from_f03 = {
        "event_id": "Ev12345678",
        "user_id": "U00000000",
        "text_content": "助けてください",
        "intent_tag": "consultation",     # ここを変えて挙動を確認する
        "status": "pending_generation"
    }
    
    # 辞書をJSON文字列に変換 (通信を模倣)
    json_b = json.dumps(mock_input_from_f03, ensure_ascii=False)
    print(f"\n📥 [Input] Data from F-03 (Mock):\n{json_b}")

    # 2. F-04 (Generator) を実行
    print("\n⚙️ [Process] Calling F-04 (Generator)...")
    try:
        json_c = generate_feedback(json_b)
        print(f"✅ F-04 Output:\n{json_c}")
    except Exception as e:
        print(f"❌ F-04 Error: {e}")
        return

    # 3. F-05 (Archive) を実行
    print("\n💾 [Process] Calling F-05 (Archive)...")
    try:
        result = archive_process(json_c)
        if result:
            print("✅ F-05 Success: Data archived.")
    except Exception as e:
        print(f"❌ F-05 Error: {e}")

    print("\n🏁 === Test Finished ===")

if __name__ == "__main__":
    main()