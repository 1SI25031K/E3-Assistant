# backend/f04_gen/generator.py
import os
import logging
from google import genai
from datetime import datetime

# 🔌 Contract Review: データクラスのインポート
from backend.common.models import SlackMessage, FeedbackResponse

# Cloud & API Ready: ローカル開発用 .env 読み込み
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

class AI_Generator:
    def __init__(self):
        # 必須環境変数のチェック (Fail Fast)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Critical: GEMINI_API_KEY is not set.")
        
        genai.configure(api_key=api_key)
        # 応答速度とコストのバランスが良いモデルを選択
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_reply(self, message: SlackMessage) -> FeedbackResponse:
        """
        SlackMessageの内容を元に、Geminiで返信を生成する。
        """
        try:
            logger.info(f"Generatig response for intent: {message.intent_tag}")

            # プロンプトの構築（意図に応じた分岐もここで可能）
            prompt = f"""
            あなたはスタートアップ支援ボット 'Slacker' です。
            以下のユーザーからの問い合わせに対し、簡潔かつフレンドリーに回答してください。
            
            ユーザーの発言: {message.text}
            """

            # Gemini API 呼び出し
            response = self.model.generate_content(prompt)
            reply_text = response.text

            # 🔌 Contract Review: FeedbackResponse オブジェクトの生成
            return FeedbackResponse(
                target_user_id=message.user_id,
                channel_id=message.channel_id,
                thread_ts=message.ts,  # 元のメッセージのTSをスレッドTSとして使用
                feedback_summary=reply_text,
                status="success",
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            # エラー時も空のオブジェクトではなく、エラー状態を返す
            return FeedbackResponse(
                target_user_id=message.user_id,
                channel_id=message.channel_id,
                thread_ts=message.ts,
                feedback_summary="申し訳ありません。AIの処理中にエラーが発生しました。",
                status="error",
                timestamp=datetime.now().isoformat()
            )

if __name__ == "__main__":
    # 動作確認
    test_msg = SlackMessage(text="Pythonのメリットは？", user_id="U123", channel_id="C123", ts="123456")
    gen = AI_Generator()
    res = gen.generate_reply(test_msg)
    print(f"AI Response: {res.feedback_summary}")