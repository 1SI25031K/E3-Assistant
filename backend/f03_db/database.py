import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from backend.common.models import SlackMessage, FeedbackResponse # 両方インポート # プロジェクト内の共通ルール（クラス定義）を読み込む
from typing import Union # 型ヒント追加


# 1. 環境変数の読み込み
load_dotenv()

# 2. DynamoDBリソースの初期化（このファイルが読まれた時点で準備する）
dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_DEFAULT_REGION"))
# 3. 操作するテーブルを特定
table = dynamodb.Table('SlackerEvents')

def save_to_db(data: Union[SlackMessage, FeedbackResponse]) -> bool:
    """
    SlackMessage または FeedbackResponse をDynamoDBに保存する
    """
    # どちらのクラスが来てもIDを取り出せるようにする
    event_id = data.event_id
    
    # ユーザーIDの取得（クラスによってフィールド名が違うため分岐）
    if isinstance(data, SlackMessage):
        u_id = data.user_id
    elif isinstance(data, FeedbackResponse):
        u_id = data.target_user_id
    else:
        u_id = "UNKNOWN"

    print(f"--- [F-03] Saving to DynamoDB: {event_id} (User: {u_id}) ---")

    try:
        # クラスオブジェクトを辞書(dict)に変換
        item_data = data.to_dict()

        # データの書き込み実行
        table.put_item(Item=item_data)
        
        print(f"✅ Data saved successfully.")
        return True

    except ClientError as e:
        print(f"AWS ClientError: {e.response['Error']['Message']}")
        return False
        
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False
