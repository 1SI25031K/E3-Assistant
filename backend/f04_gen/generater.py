import os
import google.generativeai as genai
from backend.common.models import SlackMessage, FeedbackResponse
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# Gemini APIの初期設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_feedback(message: SlackMessage) -> FeedbackResponse:
    """
    F-04: AIフィードバック生成 (クラス対応版)
    SlackMessageを受け取り、Geminiを使用してフィードバックを生成して返す。
    """
    print(f"--- F-04: Gemini API Processing (Intent: {message.intent_tag}) ---")

    # 1. プロンプトの組み立て
    # クラスのプロパティを直接参照するので、スペルミスのリスクがありません
    prompt = f"""
    あなたはスタートアップチームのAIテックリードです。
    ユーザーの意図タグ: {message.intent_tag}
    メッセージ内容: {message.text_content}

    上記に対して、具体的かつ建設的なフィードバックを1〜2文で返してください。
    """

    try:
        # 2. Gemini API 呼び出し
        model = genai.GenerativeModel("gemini-1.5-flash") # または gemini-pro
        response = model.generate_content(prompt)
        ai_text = response.text.strip()

        # 3. 返却データの作成 (FeedbackResponseクラス)
        # Contract Cの形式でオブジェクトを生成して返します
        return FeedbackResponse(
            event_id=message.event_id,
            target_user_id=message.user_id,
            feedback_summary=ai_text,
            status="complete"
        )

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        # エラー時はフォールバックの応答を返す
        return FeedbackResponse(
            event_id=message.event_id,
            target_user_id=message.user_id,
            feedback_summary="申し訳ありません。フィードバック生成中にエラーが発生しました。",
            status="error"
        )

# 🧪 単体テスト用
if __name__ == "__main__":
    # テスト用のSlackMessageオブジェクト
    test_message = SlackMessage(
        event_id="EvTEST_123",
        user_id="U_KOSEI",
        text_content="Pythonのクラス継承がいまいち分かりません。",
        intent_tag="question"
    )
    
    # 実行
    result = generate_feedback(test_message)
    
    # 結果の確認
    print("\n✅ 生成されたフィードバック:")
    print(f"宛先: {result.target_user_id}")
    print(f"内容: {result.feedback_summary}")