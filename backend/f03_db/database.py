import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from backend.common.models import SlackMessage # プロジェクト内の共通ルール（クラス定義）を読み込む

# 1. 環境変数の読み込み
load_dotenv()

# 2. DynamoDBリソースの初期化（このファイルが読まれた時点で準備する）
dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_DEFAULT_REGION"))
# 3. 操作するテーブルを特定
table = dynamodb.Table('SlackerEvents')

def save_to_db(slack_message: SlackMessage) -> bool:
    print(f"--- [F-03] Saving to DynamoDB: {slack_message.event_id} ---")

    try:
        # 4. クラスオブジェクトを辞書(dict)に変換
        # DynamoDBはPythonのクラスを直接理解できないため、
        # models.py で定義した .to_dict() メソッドを使って「翻訳」する。
        item_data = slack_message.to_dict()

        # 5. データの書き込み実行
        # put_item は「上書き保存」の挙動をする（同じIDがあれば更新される）
        table.put_item(Item=item_data)
        
        print(f"Data saved successfully for User: {slack_message.user_id}")
        return True

    except ClientError as e:
        # 6. AWS側のエラー（権限不足、ネットワーク遮断など）をキャッチ
        print(f"AWS ClientError: {e.response['Error']['Message']}")
        return False
        
    except Exception as e:
        # 7. その他の予期せぬエラー（プログラムのバグなど）をキャッチ
        print(f"Unexpected Error: {e}")
        return False

# 🧪 単体テスト用ブロック
if __name__ == "__main__":
    # テストデータを作成（本番では F-01/F-02 から渡ってくる）
    test_msg = SlackMessage(
        event_id="TEST_DB_001",
        user_id="U_TEST_USER",
        text_content="DynamoDBへの書き込みテストです。",
        intent_tag="test",
        status="testing"
    )
    
    # 保存を実行
    save_to_db(test_msg)
