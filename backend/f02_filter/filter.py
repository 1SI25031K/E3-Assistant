import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv  # .envを読み込むための道具
from backend.common.models import SlackMessage

# ロガー設定
logger = logging.getLogger(__name__)

# ここで念のため .env を読み込みます
load_dotenv()

def analyze_intent(input_message: SlackMessage) -> SlackMessage:
    """
    [F-02] Geminiを使って、メッセージが「質問」か「雑談」かを判定する
    """
    logger.info(f"--- [F-02] Analyzing Intent for: {input_message.event_id} ---")

    text = input_message.text_content
    
    # ▼▼▼【ここが修正のキモ！】▼▼▼
    # プログラムの最初ではなく、「この関数が呼ばれた瞬間」にキーを取得します。
    # これなら読み込み順序に関係なく確実に取得できます。
    api_key = os.environ.get("GEMINI_API_KEY")
    # ▲▲▲ ------------------------

    # APIキーがない場合はキーワード判定に逃げる
    if not api_key:
        logger.warning("⚠️ API Key not found. Fallback to keyword matching.")
        if "?" in text or "教えて" in text or "質問" in text or "コード" in text:
            input_message.intent_tag = "question"
        else:
            input_message.intent_tag = "chat"
        return input_message

    try:
        # Geminiの設定
        genai.configure(api_key=api_key)
        
        # 軽量モデルを使用
        model = genai.GenerativeModel("gemini-2.5-flash")

        # プロンプト（AIへの指示書）
        prompt = f"""
        あなたはSlackボットの「意図判定」システムです。
        以下のメッセージを読み、それが「回答が必要な質問・相談・エラー報告」か「ただの雑談・挨拶」か分類してください。
        
        メッセージ: "{text}"
        
        出力ルール:
        - 質問、作業依頼、エラー報告なら "question" とだけ出力してください。
        - 挨拶、相槌、独り言なら "chat" とだけ出力してください。
        - 余計な説明は一切不要です。単語一つだけを返してください。
        """

        response = model.generate_content(prompt)
        intent = response.text.strip().lower()
        
        # 結果に応じたタグ付け
        if "question" in intent:
            final_tag = "question"
        else:
            final_tag = "chat"

        logger.info(f"🤖 AI Judgment: '{text}' => {final_tag}")

        input_message.intent_tag = final_tag
        return input_message

    except Exception as e:
        logger.error(f"❌ Intent Analysis Error: {e}")
        # エラー時は安全策として question にしておく
        input_message.intent_tag = "question"
        return input_message