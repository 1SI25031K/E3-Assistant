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
    print(f"--- 🧠 [F-04] Gemini Thinking... (Intent: {message.intent_tag}) ---")

    try:
        # 3. プロンプト（命令文）の構築
        system_instruction = """
        あなたはスタートアップチームの開発を支援する優秀なAIテックリード「Slacker」です。
        以下の制約を守って回答してください。
        
        1. 初心者にも分かりやすく、かつ技術的に正確なアドバイスをすること。
        2. 常に励ますような、ポジティブなトーンを維持すること。
        3. 回答は簡潔に、要点を絞って伝えること（長文は避ける）。
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
    print("🚀 F-04 Gemini Connection Test (New Client)")
    
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
    
    print("\n🤖 生成された回答:")
    print("--------------------------------------------------")
    print(result.feedback_summary)
    print("--------------------------------------------------")