import sys
import os

# プロジェクトのルートディレクトリをパスに追加（モジュール読み込み用）
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from backend.common.models import SlackMessage

def analyze_intent(message: SlackMessage) -> SlackMessage:
    
    print(f"--- [F-02] Analyzing Intent for: {message.event_id} ---")
    
    # 1. テキストの正規化
    # 全角スペースを半角にしたり、小文字に統一したりして、判定ミスを減らす
    text = message.text_content.strip().lower()
    
    # 2. ルールベースによる判定ロジック
    # 本来はAI(BERT等)を使う場所だが、開発初期は「キーワード判定」が最も速くて確実。
    
    # パターンA: 質問 (Question)
    # 「？」や具体的な質問ワードが含まれる場合
    if any(word in text for word in ["?", "？", "教えて", "どうすれば", "error", "エラー", "実装"]):
        new_tag = "question"
        
    # パターンB: 相談 (Consultation)
    # 「相談」「悩み」「助けて」など、少し深刻または長めの議論が必要な場合
    elif any(word in text for word in ["相談", "悩み", "聞いて", "困って", "help"]):
        new_tag = "consultation"
        
    # パターンC: 雑談 (Chat)
    # 上記に当てはまらないものは、とりあえず雑談として扱う
    else:
        new_tag = "chat"

    # 3. 結果の適用
    # オブジェクトの中身（タグ）を書き換える
    message.intent_tag = new_tag
    
    print(f"Intent determined: {new_tag}")
    
    # 加工したオブジェクトを次の工程（F-03, F-04）へ返す
    return message

# 🧪 単体テスト用
if __name__ == "__main__":
    # テストデータ
    test_msg = SlackMessage(
        event_id="TEST_FILTER_001",
        user_id="U_TEST",
        text_content="Pythonの環境構築でエラーが出ます。教えてください。",
        intent_tag="tbd", # 最初は不明(To Be Determined)
        status="pending"
    )
    
    # 実行
    result = analyze_intent(test_msg)
    
    print(f"入力テキスト: {test_msg.text_content}")
    print(f"判定結果: {result.intent_tag}")
