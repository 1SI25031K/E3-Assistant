# Emysys Project - Developer Guide (Ver 2.0)

## 1. プロジェクト概要
**Slacker**は、スタートアップチームの「具体性の欠如」と「連携不全」を解決するためのAIアシスタントシステムである。
本ドキュメントは、**2025年12月11日のPhase 1（データ開通）マイルストーン**を達成するための技術的な憲法である。

---

## 2. チーム構成と担当領域 (Roles)

| ID | 機能モジュール | 担当者 | 役割 (Role) | 責務 (Responsibility) |
|:--|:---|:---|:---|:---|
| **F-01** | **Listener** | **ユウリ** | I/O (Input) | SlackからのWebhook受信、Payloadの正規化 |
| **F-02** | **Filter** | **コウタ** | Filter | ユーザー意図の判定 (Intent Classification) |
| **F-03** | **Persistence** | **コウタ** | DB | データの永続化、ステータス管理 |
| **F-04** | **Gen (Core)** | **コウセイ** | Logic | AIによるフィードバック生成 |
| **F-05** | **Archive** | **コウセイ** | Archive | ログ保存、学習データ蓄積 |
| **F-06** | **Notify** | **ユウリ** | I/O (Output) | Slackへのレスポンス送信 |

---

## 3. ディレクトリ構造 (Directory Structure)
以下の構造を厳守すること。ファイル名やフォルダ名を勝手に変更してはならない。

```text
Emysys/
├── README.md           # 本ドキュメント
├── docker-compose.yml  # ローカル開発環境用
├── backend/
│   ├── f01_listener/   # [ユウリ] main.py (FastAPI/Flask)
│   ├── f02_filter/     # [コウタ] logic.py
│   ├── f03_db/         # [コウタ] models.py, crud.py
│   ├── f04_gen/        # [コウセイ] generator.py
│   ├── f05_archive/    # [コウセイ] logger.py
│   └── f06_notify/     # [ユウリ] slack_client.py
└── docs/               # 設計書など

```

## 4. インターフェース定義 (The Contract)
各モジュール間のデータ受け渡しは「バケツリレー」方式で行う。以下のJSONスキーマ以外のデータが流れることは許容されない。

### Contract A: F-01 (Listener) ➔ F-02 (Filter)
**Slackの生Payloadを整形し、下流工程が扱いやすい形にする。**

```json
{
  "source": "slack",                // 固定値
  "event_id": "Ev00000000",         // Slackの一意なイベントID (トレーサビリティ用)
  "user_id": "U00000000",           // 発言したユーザーID
  "text_content": "助けてください"    // ユーザーのメッセージ本文
}
```
### Contract B: F-02/03 (Filter/DB) ➔ F-04 (Gen)
**意図判定タグと処理ステータスを付与してコアロジックへ渡す。**

```json
{
  "event_id": "Ev00000000",
  "user_id": "U00000000",
  "text_content": "助けてください",
  "intent_tag": "consultation",     // "consultation" | "report" | "chat"
  "status": "pending_generation"    // DB保存時のステータス
}
```

### Contract C: F-04 (Gen) ➔ F-06 (Notify)
**生成されたフィードバックと、通知先情報をまとめる。**
```json
{
  "event_id": "Ev00000000",
  "target_user_id": "U00000000",       // 返信先のユーザーID (= user_id)
  "feedback_summary": "具体性を上げてください", // 生成されたテキスト
  "status": "complete"
}
```



