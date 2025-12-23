import os
import sys
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# プロジェクトのルートディレクトリをパスに追加（モジュール読み込み用）
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from backend.common.models import FeedbackResponse

# 1. 環境変数の読み込み (.envからシークレット類を取得)
load_dotenv()

# 2. Slackクライアントの初期化 (グローバルスコープで一度だけ行う)
slack_token = os.getenv("SLACK_BOT_TOKEN")
# WebClientはSlack APIと通信するための公式の道具箱
client = WebClient(token=slack_token)

def send_reply(response: FeedbackResponse) -> bool:
    """
    [F-06] Slackへの返信送信
    
    Backendの最終工程。FeedbackResponseオブジェクトを受け取り、
    指定されたユーザー(target_user_id)に対してメッセージを送信する。
    
    Args:
        response (FeedbackResponse): 送信したいデータ
        
    Returns:
        bool: 送信に成功したらTrue
    """
    print(f"--- 📤 [F-06] Sending Reply to Slack: {response.target_user_id} ---")

    try:
        # 3. メッセージ送信の実行
        # chat_postMessage は最も基本的な「発言」メソッド
        result = client.chat_postMessage(
            channel=response.target_user_id,  # 宛先 (ユーザーID または チャンネルID)
            text=response.feedback_summary    # 本文 (AIが生成したテキスト)
        )
        
        # Slack APIからの応答に含まれる "ok" フィールドを確認
        if result["ok"]:
            print(f"✅ Message sent successfully to {response.target_user_id}")
            return True
        else:
            print(f"❌ Message sent but marked as failed: {result}")
            return False

    except SlackApiError as e:
        # 4. Slack特有のエラーハンドリング
        # 権限不足(missing_scope)や宛先不明(channel_not_found)などがここで補足される
        print(f"❌ Slack API Error: {e.response['error']}")
        return False
        
    except Exception as e:
        # その他の予期せぬエラー
        print(f"❌ Unexpected Error in F-06: {e}")
        return False

# 🧪 単体テスト用ブロック
if __name__ == "__main__":
    print("🚀 F-06 Standalone Test")
    
    # テスト送信先ID (自分のIDなど) を .env またはここに直接指定
    # ※本番ではF-01が取得したIDが入る
    TEST_TARGET_ID = os.getenv("TEST_USER_ID", "U01234567") 

    if slack_token and slack_token.startswith("xoxb-"):
        # テストデータの作成
        test_data = FeedbackResponse(
            event_id="TEST_NOTIFY_001",
            target_user_id=TEST_TARGET_ID,
            feedback_summary="【F-06テスト】\nこれはPythonプログラムから送信されたテストメッセージです。\n正常に届いていますか？",
            status="complete"
        )
        
        # 実行
        send_reply(test_data)
    else:
        print("⚠️ SLACK_BOT_TOKEN が正しく設定されていません。.envを確認してください。")
