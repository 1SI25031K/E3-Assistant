"""
AWS Lambda ハンドラー
FlaskアプリケーションをLambda環境で実行するためのエントリーポイント
"""
import os
import sys
from pathlib import Path

# Lambda環境でも動作するようにパスを設定
# Lambdaのランタイムでは /var/task が作業ディレクトリになる
backend_dir = Path(__file__).parent
project_root = backend_dir.parent

# プロジェクトルートをパスに追加
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 環境変数の読み込み（Lambda環境では環境変数が直接設定されるため、dotenvはオプション）
# ローカル開発時のみ .env ファイルから読み込む
if os.path.exists(project_root / ".env"):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=project_root / ".env")

# Flaskアプリのインポート（パス設定後に実行）
from backend.f01_listener.server import app

# mangumを使用してFlaskアプリをASGIアプリとしてラップ
# mangumはFlaskアプリを自動的にASGIアダプターでラップします
from mangum import Mangum

# Lambdaハンドラーとして公開
# lifespan="off" はFlaskアプリがASGI lifespanイベントを必要としないため
handler = Mangum(app, lifespan="off")
