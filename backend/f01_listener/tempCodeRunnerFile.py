import json
import datetime

def main():
    """
    F-01: Slack Listener (Mock Version)
    本物のSlack APIの代わりに、固定のダミーデータを生成して標準出力します。
    """
    
    # 1. データの作成
    # ここが「バケツの中身」です。READMEの定義通りに作ります。
    mock_data = {
        "source": "slack",
        "event_id": "evt_dummy_12345",  # テスト用の適当なID
        "user_id": "U_TEST_USER_01",    # テスト用のユーザーID
        "timestamp": datetime.datetime.now().isoformat(), # 現在時刻を文字列にする
        "text_content": "これはユウリのF-01から送られたテストメッセージです。コウタさん、データは届いていますか？"
    }

    # 2. データの出力 (Output)
    # Pythonの辞書データ(dict)を、文字としてのJSON形式(string)に変換して表示します。
    # ensure_ascii=False は、日本語を正しく表示させるためのおまじないです。
    json_output = json.dumps(mock_data, ensure_ascii=False, indent=2)
    
    # 標準出力(画面)に出すことで、次のプログラムがこれを受け取れるようになります。
    print(json_output)
    return json_output

if __name__ == "__main__":
    main()

