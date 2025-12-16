

import json

def generate_feedback(json_str):
    """
    Contract B (JSON文字列) を受け取り、
    AIによるフィードバック結果を含む Contract C (JSON文字列) を返す。
    """
    # 1. 入力を受け取る (Contract B)
    # ここでエラーが出るなら、コウタさんからのデータがおかしいということになる
    input_data = json.loads(json_str)
    
    intent = input_data.get("intent_tag")
    text = input_data.get("text_content")
    
    print(f"--- F-04: Generating feedback for intent='{intent}' ---")

    # 2. ロジック実行 (Mock)
    # 本来はここでLLMを呼び出すが、まずは条件分岐でダミー応答を作る
    feedback_text = ""
    
    if intent == "question":
        feedback_text = f"【AI回答】ご質問「{text}」について回答します。Wikiのこのページを参照してください。"
    elif intent == "report":
        feedback_text = "【AI回答】日報ありがとうございます。進捗は順調ですね！"
    elif intent == "consultation":
        feedback_text = f"【AI回答】「{text}」という相談ですね。後ほど担当者から連絡します。"
    else:
        feedback_text = f"【AI回答】メッセージを受け取りました。（タグ: {intent}）"

    # 3. 出力を作成 (Contract C)
    # F-06 (Notify) が必要とする情報を詰める
    output_data = {
        "event_id": input_data.get("event_id"),
        "target_user_id": input_data.get("user_id"), # 返信先
        "feedback_summary": feedback_text,
        "status": "complete"
    }
    
    # JSON文字列にして返す
    return json.dumps(output_data, ensure_ascii=False, indent=2)

# 単体テスト用（このファイルを直接実行した時だけ動く）
if __name__ == "__main__":
    # テスト用データ (Contract B)
    test_input = json.dumps({
        "event_id": "EvTEST",
        "user_id": "U_TEST",
        "text_content": "テスト",
        "intent_tag": "question",
        "status": "pending"
    })
    print(generate_feedback(test_input))