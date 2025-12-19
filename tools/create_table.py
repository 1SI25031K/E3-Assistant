import os
import boto3
from dotenv import load_dotenv

# 1. .envから環境変数を読み込む
load_dotenv()

def create_slacker_table():
    # 2. DynamoDBのリソースオブジェクトを取得
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_DEFAULT_REGION"))

    try:
        # 3. テーブル作成の命令を出す
        table = dynamodb.create_table(
            TableName='SlackerEvents',  # テーブル名
            # 4. キーの役割（スキーマ）を定義
            KeySchema=[
                {
                    'AttributeName': 'event_id',
                    'KeyType': 'HASH'  # HASH = パーティションキー
                }
            ],
            # 5. キーとして使う属性の「型」を定義
            AttributeDefinitions=[
                {
                    'AttributeName': 'event_id',
                    'AttributeType': 'S'  # S = String（文字列）
                }
            ],
            # 6. 課金モードと性能の設定
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        # 7. テーブルが作成完了（Active）になるまで待機
        print("⌛ テーブル作成中...")
        table.wait_until_exists()
        print(f"✅ テーブル {table.table_name} が正常に作成された。")

    except Exception as e:
        print(f"❌ エラーが発生した: {e}")

if __name__ == "__main__":
    create_slacker_table()

