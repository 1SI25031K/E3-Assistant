# backend/f05_archive/main.py
import json
import datetime
import os

# F-04 (Generator) から渡ってくるはずのデータ（ダミー）
mock_input_from_f04 = """
{
  "source": "slack",
  "event_id": "evt_123456789",
  "user_id": "U0123456",
  "text_content": "明日のMTG資料はどこですか？",
  "intent_tag": "question",
  "status": "processed",
  "target_user_id": "U0123456",
  "feedback_summary": "【自動応答】Wikiをご確認ください。",
  "original_event_id": "evt_123456789"
}
"""

def archive_process(json_str):
    data = json.loads(json_str)
    
    # アーカイブ時刻を付与
    data["archived_at"] = datetime.datetime.now().isoformat()

    # ローカルファイルに追記保存 (JSON Lines形式)
    # これが簡易DBの代わりになります
    log_file = "local_history.jsonl"
    
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        
        print(f"--- F-05: Data archived to {log_file} ---")
        return True
        
    except Exception as e:
        print(f"Error archiving data: {e}")

if __name__ == "__main__":
    archive_process(mock_input_from_f04)