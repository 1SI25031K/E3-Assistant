import sys
import os
import google.generativeai as genai
from dotenv import load_dotenv

# プロジェクトのルートディレクトリをパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

# .envを読み込む
env_path = os.path.join(root_dir, ".env")
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print(f"🔑 API Key Status: {'OK' if api_key else 'Missing'}")
print("📋 利用可能なモデル一覧:")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")