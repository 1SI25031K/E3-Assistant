# backend/f04_generator/main.py
import json

# コウタさん(F-02)から渡ってくるはずのデータ（ダミー）
# ※ここが「Contract」です。彼がこの形式を守る前提であなたは動きます。
mock_input_from_f02 = """
{
  "source": "slack",
  "event_id": "evt_123456789",
  "user_id": "U0123456",
  "text_content": "明日のMTG資料はどこですか？",
  "intent_tag": "question",
  "status": "processed"
}
"""

def generate_feedback(json_str):
    data = json.loads(json_str)
    
    print(f"--- F-04: Generating feedback for tag '{data.get('intent_tag')}' ---")

    # 本来はLLM (OpenAI API) を呼び出しますが、Phase 1ではロジックのみ実装します
    intent = data.get("intent_tag")
    user_content = data.get("text_content")
    
    generated_text = ""
    
    if intent == "question":
        generated_text = f"【自動応答】ご質問ありがとうございます。「{user_content}」については、Wikiをご確認ください。"
    elif intent == "task_report":
        generated_text = "【自動応答】日報の提出を確認しました。お疲れ様です！"
    else:
        generated_text = "【自動応答】メッセージを受け取りました。"

    # F-06 (Notifer) へ渡すためのデータを構成
    # Contract: target_user_id と feedback_summary が必須
    output_data = {
        "target_user_id": data["user_id"],
        "feedback_summary": generated_text,
        "original_event_id": data["event_id"]
    }
    
    output_json = json.dumps(output_data, ensure_ascii=False, indent=2)
    
    # 人間確認用
    print("--- F-04 Output ---")
    print(output_json)
    
    # ★ここを追加！ 次の走者(F-05)にバトンを渡す
    return output_json

if __name__ == "__main__":
    generate_feedback(mock_input_from_f02)