import os
import logging
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from typing import Optional
from backend.common.models import SlackMessage, FeedbackResponse

# ローカル開発時のみ .env を読み込む
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

class DynamoDBHandler:
    def __init__(self):
        self.region = os.getenv("AWS_DEFAULT_REGION", "ap-northeast-1")
        self.table_name = os.getenv("DYNAMODB_TABLE", "SlackerFeedback")
        
        try:
            # IAM認証: aws_access_key_id 等を指定しないことで、
            # 自動的に実行環境（ローカルなら .aws/credentials、AWSなら IAMロール）の権限を見に行きます。
            self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
            self.table = self.dynamodb.Table(self.table_name)
            logger.info(f"DB initialized. Table: {self.table_name}, Region: {self.region}")
        except Exception as e:
            logger.error(f"Failed to connect to DynamoDB: {e}")
            raise

    def save_log(self, message: SlackMessage, feedback: Optional[FeedbackResponse] = None):
        """
        ログを保存または更新。
        SlackMessageの状態（status）や、FeedbackResponseの有無に応じてレコードを更新。
        Primary Key: ts (Slackのタイムスタンプ) - これを一意なIDとして扱う
        """
        if not message.ts:
            logger.error("Timestamp (ts) is missing. Cannot save to DB.")
            return

        # 基本情報の構築
        item = {
            'ts': message.ts,          # Partition Key (PK)
            'user_id': message.user_id,
            'channel_id': message.channel_id,
            'text': message.text,
            'status': message.status,  # "pending" -> "done" 等の状態遷移
            'intent_tag': message.intent_tag,
            'updated_at': datetime.now().isoformat()
        }

        # Feedbackがある場合は結合する
        if feedback:
            item['feedback_summary'] = feedback.feedback_summary
            item['response_timestamp'] = feedback.timestamp or datetime.now().isoformat()
        
        try:
            # put_item は「上書き保存」です。キー(ts)が同じなら更新、なければ新規作成されます。
            # update_item よりもロジックが単純で、データの整合性を保ちやすいアプローチです。
            self.table.put_item(Item=item)
            logger.info(f"Record saved for ts={message.ts}, status={message.status}")
            
        except ClientError as e:
            logger.error(f"DynamoDB ClientError: {e.response['Error']['Message']}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in save_log: {e}")
            raise

if __name__ == "__main__":
    # 動作確認用（ローカルでAWS接続情報がある場合のみ動作）
    print("Testing DynamoDBHandler...")
    try:
        handler = DynamoDBHandler()
        test_msg = SlackMessage(
            text="AWS接続テスト", 
            user_id="U_TEST", 
            channel_id="C_TEST", 
            ts="1700000000.000001",
            status="testing"
        )
        handler.save_log(test_msg)
        print("Test passed: Item saved.")
    except Exception as e:
        print(f"Test failed: {e}")
        print("Note: ローカルで実行する場合、AWS CLIの設定(~/.aws/credentials)が必要です。")