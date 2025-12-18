# Slacker Project - Developer Guide 

## 1. プロジェクト概要
**Slacker**は、スタートアップチームの「具体性の欠如」と「連携不全」を解決するためのAIアシスタントシステムである。

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
├── .env                # トークン・設定値 (宮本が配布)
├── main.py             # パイプライン全体の実行エントリーポイント
└── backend/
    ├── common/         # 共通定義
    │   └── models.py   # データクラス (SlackMessage, FeedbackResponse)
    ├── f01_listener/   # [近藤]
    ├── f02_filter/     # [蘇木]
    ├── f03_db/         # [近藤]
    ├── f04_gen/        # [宮本]
    ├── f05_archive/    # [宮本]
    └── f06_notify/     # [近藤]
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


MTGでの森重さんのアドバイスと、README（プロジェクト憲法）の定義に基づき、コウセイさん（F-04/F-05担当）が**「他メンバーの進捗を待たずに」**直ちに着手すべきタスクをリストアップしました。

これらをコピーして、自身のToDoリストやDiscordの進捗報告に使用してください。

---



### 宮本航聖のタスク

#### 1. チームマネジメント

#### 2. インターフェース（Contract）の合意形成

* [ ] **Contract B (F-03 ➔ F-04)** のJSON形式を確定する
* READMEの定義 に基づき、`intent_tag` や `status` を含むJSONサンプルを作成する。

* [ ] 作成したJSONサンプルをDiscordでコウタ（F-02/03）に共有し、合意をとる

#### 3. F-04 (Generator) のスタンドアロン実装

* [ ] `backend/f04_gen/main.py` を修正・実装する
* [ ] 入力として **Contract B** のJSONを受け取る処理を書く
* [ ] 内部ロジック（`intent_tag` に応じた分岐）を実装する（※最初はif文による静的な応答でOK）
* [ ] 出力として **Contract C** (`target_user_id`, `feedback_summary` 等) のJSONを返す処理を書く

#### 4. F-05 (Archive) の実装

* [ ] `backend/f05_archive/main.py` を実装する
* [ ] 入力として **Contract C** のJSONを受け取る
* [ ] ローカルファイル（`local_history.jsonl` 等）にデータを追記保存する処理を書く

#### 5. オーケストレーター (`backend/main.py`) の作成

* [ ] `backend/` 直下に `main.py` を新規作成する（`run_pipeline.py` とは別物として作る）
* [ ] `main.py` 内部に、F-03から来るはずのデータを模した**ダミー変数（Mock Data）**を定義する
* [ ] そのダミーデータを引数に `f04_gen` を呼び出し、その結果を `f05_archive` に渡す一連の流れを記述する
* [ ] ローカル環境で `python backend/main.py` を実行し、エラーなく動作することを確認する

#### 6. Slack Bot (Entrance) の準備

* [ ] Slackアプリ（Bot）を作成し、トークンを取得する
* [ ] メンションやボタン押下をトリガーにして、上記の `main.py` が起動する仕組みを実装する（※まずはローカルで動作すればOK）


