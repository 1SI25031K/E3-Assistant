import sys
import os
import google.generativeai as genai
from dotenv import load_dotenv

# プロジェクトのルートディレクトリをパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

# 🔌 接続チェック
from backend.common.models import SlackMessage

# .envを読み込む
env_path = os.path.join(root_dir, ".env")
load_dotenv(env_path)

# APIキー設定
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print(f"⚠️ 警告: {env_path} に GEMINI_API_KEY が見つかりません！")
else:
    genai.configure(api_key=api_key)

def ask_gemini_is_question(text: str) -> bool:
    """
    Gemini API (google-generativeai) を使って判定する
    """
    if not api_key:
        return False

    try:
        # ★ここを修正しました！リストにあった最新モデルを指定
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        あなたは社内Slackの優秀なアシスタントです。
        以下のメッセージが「技術的な質問」や「回答が必要な問い合わせ」であれば 'YES' を、
        単なる「雑談」や「挨拶」、「報告」であれば 'NO' を返してください。
        
        メッセージ: "{text}"
        
        回答 (YES または NO のみ):
        """

        # AIに聞く
        response = model.generate_content(prompt)
        answer = response.text.strip().upper()
        
        print(f"🤖 [AI判定] Answer: {answer} | Text: {text}")
        return "YES" in answer

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return False

def analyze_intent(message: SlackMessage) -> SlackMessage:
    text = message.text_content
    
    # AI判定を実行
    is_question = ask_gemini_is_question(text)

    if is_question:
        message.intent_tag = "question"
        message.status = "processing"
        print(f"🔍 [Filter] Intent detected: QUESTION (User: {message.user_id})")
    else:
        message.intent_tag = "chat"
        message.status = "ignored"
        print(f"💤 [Filter] Intent detected: CHAT (User: {message.user_id})")

    return message

# --- 動作確認用 ---
if __name__ == "__main__":
    test_msgs = [
        SlackMessage(event_id="1", user_id="U1", text_content="Pythonでリストをソートする方法は？"),
        SlackMessage(event_id="2", user_id="U2", text_content="おはようございます！"),
        SlackMessage(event_id="3", user_id="U3", text_content="Dockerのビルドエラーが解決できません。"),
    ]
    
    print(f"--- AI判定テスト開始 (Key check: {'OK' if api_key else 'NG'}) ---")
    for msg in test_msgs:
        analyze_intent(msg)
        print("-" * 20)