import os
from google import genai
from dotenv import load_dotenv
from backend.common.models import SlackMessage, FeedbackResponse

# 1. 環境変数の読み込み
load_dotenv()

# 2. Gemini APIの設定 (新ライブラリ版)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 新しいクライアントの初期化
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_feedback(message: SlackMessage) -> FeedbackResponse:
    """
    [F-04] AIフィードバック生成 (google-genai 新ライブラリ対応版)
    """
    print(f"--- [F-04] Gemini Thinking... (Intent: {message.intent_tag}) ---")

    try:
        # 3. プロンプト（命令文）の構築
        system_instruction = """

## 役割
あなたは高度なエンジニアリング・コミュニケーションの専門家「E3-Assistant」です。
Slack上の質問者と回答者のやり取りを解析し、両者の技術的成長を最大化するための、厳格かつ建設的なフィードバックを提供してください。

## 制約事項
- 挨拶（「こんにちは」「お疲れ様です」等）は一切禁止。
- 絵文字は一切禁止。
- 結論から述べ、箇条書きで簡潔に構成すること。
- 「優しさ」よりも「改善点の具体性」を優先すること。

## 評価・フィードバック基準
1. 質問者へのフィードバック:
   - 背景が共有されているか。
   - 試したことが明記されているか。
   - 期待値と実測値の差分が明確か。
2. 回答者へのフィードバック:
   - 答えを直接与えすぎていないか（考え方を提示しているか）。
   - 参照すべき公式ドキュメントやキーワードを提示しているか。

## 出力フォーマット
【スコア】質問: X/10, 回答: X/10
【質問者への改善点】
- (具体的な改善アクション)
【回答者への改善点】
- (具体的な改善アクション)        


        """
        
        user_query = f"""
        【ユーザーの状況】
        ユーザーID: {message.user_id}
        意図タグ: {message.intent_tag}
        
        【メッセージ内容】
        {message.text_content}
        """
        
        # 4. 生成実行 (新ライブラリの構文)
        # model引数でモデル名を指定します
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_instruction}\n\n{user_query}"
        )
        
        # 結果のテキストを取り出す
        ai_text = response.text.strip()

        # 5. Contract C の作成
        return FeedbackResponse(
            event_id=message.event_id,
            target_user_id=message.user_id,
            feedback_summary=ai_text,
            status="complete"
        )

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return FeedbackResponse(
            event_id=message.event_id,
            target_user_id=message.user_id,
            feedback_summary="申し訳ありません。AI接続エラーが発生しました。後でもう一度お試しください。",
            status="error"
        )

# 🧪 単体テスト用
if __name__ == "__main__":
    print("F-04 Gemini Connection Test (New Client)")
    
    # テストデータ
    test_msg = SlackMessage(
        event_id="TEST_GEN_002",
        user_id="U_TEST_LEADER",
        text_content="Pythonの新しいライブラリへの移行について、メリットを教えて。",
        intent_tag="question",
        status="pending"
    )
    
    # 実行
    result = generate_feedback(test_msg)
    
    print("\n生成された回答:")
    print("--------------------------------------------------")
    print(result.feedback_summary)
    print("--------------------------------------------------")