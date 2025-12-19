import os
import boto3
from dotenv import load_dotenv

# 1. .envの内容を環境変数として読み込む
load_dotenv()

def test_aws_connection():
    print("--- AWS Connection Test Start ---")
    
    try:
        # 2. AWSサービスへの接続窓口（リソース）を作成
        # 引数を指定しなくても、boto3が自動的に環境変数の
        # AWS_ACCESS_KEY_ID などを探しにいってくれる
        dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_DEFAULT_REGION"))
        
        # 3. 現在のテーブル一覧を取得してみる（空でも成功すれば通信はOK）
        tables = list(dynamodb.tables.all())
        
        print(f"✅ Connection Successful!")
        print(f"現在のテーブル数: {len(tables)}")
        for table in tables:
            print(f"- {table.name}")
            
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_aws_connection()