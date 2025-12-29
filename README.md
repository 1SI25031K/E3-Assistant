# Slacker 

## 1. プロジェクト概要
**Slacker**は、スタートアップチームの「具体性の欠如」と「連携不全」を解決するためのAIアシスタントシステムである。

---

## 2. チーム構成と担当領域

| ID | 機能モジュール | 担当者 | 役割 (Role) | 責務 (Responsibility) |
|:--|:---|:---|:---|:---|
| **F-01** | **Listener** | **ユウリ** | I/O (Input) | SlackからのWebhook受信、Payloadの正規化 |
| **F-02** | **Filter** | **コウタ** | Filter | ユーザー意図の判定 (Intent Classification) |
| **F-03** | **Persistence** | **コウセイ** | DB | データの永続化、ステータス管理 |
| **F-04** | **Gen (Core)** | **コウセイ** | Logic | Gemini API を使用したフィードバック生成 |
| **F-05** | **Archive** | **コウセイ** | Archive | AWS DB への全ログ蓄積実装 |
| **F-06** | **Notify** | **コウセイ** | I/O (Output) | Slackへのレスポンス送信 |

---

## 3. ディレクトリ構造

```text
Slacker/
├── README.md           # 本ドキュメント
├── .env                # トークン・設定値 (宮本が配布)
└── backend/
　　　　　├── main.py             # プロジェクト全体の「指揮者」。各モジュールを呼び出し実行する。
　　　　　├── common/             # チーム全員が使う「共通の道具箱」。
　　　　　│   └── models.py       # データクラス定義 (SlackMessage, FeedbackResponse)
　　　　　├── f01_listener/       # [F-01] 入口：SlackからのWebhookを受け取る。
　　　　　│   ├── server.py       # 外部（Slack）からの通信を待ち受けるサーバー
　　　　　│   └── listener.py     # 受信した複雑なデータを「SlackMessage」型に変換する
　　　　　├── f02_filter/         # [F-02] 判定：メッセージが「質問」か「雑談」かを分ける。
　　　　　│   └── filter.py       # 判定ロジックの実装本体
　　　　　├── f03_db/             # [F-03] 保存/読込：データをDB（またはJSONL）に書き込む。
　　　　　│   └── database.py     # データの保存、ステータス更新の実行
　　　　　├── f04_gen/            # [F-04] 心臓部：AI（Gemini）がフィードバックを作る。
　　　　　│   └── generator.py    # Gemini APIを呼び出す生成ロジック
　　　　　├── f05_archive/        # [F-05] 記録：将来の学習用に全てのログを保存する。
　　　　　│   └── logger.py       # ログファイル（JSONL）への書き込み処理
　　　　　└── f06_notify/         # [F-06] 出口：完成したフィードバックをSlackに送り返す。
            └── notifier.py     # Slack APIを使用してメッセージを送信する
```

| フォルダ名 | 主要ファイル | 役割・責務 |
|:---|:---|:---|
| `common/` | `models.py` | チーム共通のデータ型（Class）定義。 |
| `f01_listener/` | `server.py` | Slack Webhookの受信（Flask等）。 |
| | `listener.py` | 受信データを `SlackMessage` オブジェクトへ変換。 |
| `f02_filter/` | `filter.py` | メッセージ内容から `intent_tag` を決定する。 |
| `f03_db/` | `database.py` | データの保存およびステータス管理。 |
| `f04_gen/` | `generator.py` | `SlackMessage` を元にGeminiで回答を生成。 |
| `f05_archive/` | `logger.py` | 最終結果を `local_history.jsonl` に追記保存。 |
| `f06_notify/` | `notifier.py` | `FeedbackResponse` をSlack APIで送信。 |

## 4. インターフェース定義
各モジュール間のデータ受け渡しは backend/common/models.py に定義されたクラスのインスタンスで行う。

### Contract: 入力系
**Slackからの入力、意図判定、ステータス管理に使用。**

```Python
@dataclass
class SlackMessage:
    event_id: str
    user_id: str
    text_content: str
    intent_tag: Optional[str]  # "consultation" | "report" | "chat"
    status: str                # 処理状況
```
### Contract: 出力系
**AI生成結果の通知に使用。**

```Pthon
@dataclass
class FeedbackResponse:
    event_id: str
    target_user_id: str
    feedback_summary: str
    status: str
```

## 5. 開発フローとルール
**開発環境**

外部連携時のみJSON: Slackとの送受信時以外は、常にクラスベースでデータを扱う。

ENVファイルの活用: トークン等の秘匿情報は .env に記述し、コードに直接書かない。

**ブランチ戦略**

個人ブランチ: メンバーは各自の名前でブランチを作成（例: dev-miyamoto）。

コミット: 頻繁なコミットとプッシュを実施し、進捗を可視化する。

マージ: 共通機能（クラス定義等）は main ブランチへ集約する。

**スケジュール**

完了期限: 12月26日（金） (予備日: 12月29日)

進捗報告: 問題発生時は即座にDiscordで報告し、停滞を避ける。

---



### 宮本航聖のタスク

#### 1. インフラ・API統合

[ ] AWS環境構築: データベース（RDSまたはDynamoDB）のセットアップと接続実装。

[ ] Gemini API統合: generator.py の本格実装とプロンプトチューニング。

[ ] Slack API接続: ユウリさんのモジュールに Slack SDK を組み込み、実送受信を可能にする。

[ ] テスト用Slack環境: テスト用ワークスペース/Botのセットアップとメンバーへの開放。

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



＜＜12/29追記＞＞


#### 1. 反応ロジックの強化（メンションなし起動）

* **[Slack API設定] `Event Subscriptions` の変更**
* `app_mention` だけでなく、`message.channels` イベントを購読するよう変更する。

* **[F-01 Listener] `server.py` の修正**
* メンションだけでなく、通常のメッセージイベント（`type: "message"`）も拾えるようにコードを拡張する。

* **[F-02 Filter] `filter.py` の判定キーワード追加**
* 指示のあった「"?", "？", "ですか"」などの文字列が含まれている場合のみ `status="pending"` とし、それ以外は無視するロジックを組む。

#### 2. クラウド環境（AWS / Oracle）へのデプロイ準備

ngrokを卒業し、24時間稼働するサーバーへ移行します。

* **[共通] サーバー環境の Docker 化**
* `Dockerfile` を作成し、ローカル環境（Python 3.12）をそのままクラウドへ持ち込めるようにパッケージングする。

* **[AWSの場合] App Runner**
* **App Runner:** Flaskをそのまま動かす。

* **[共通] .env（秘匿情報）の移行**
* AWS Secrets Manager や、クラウド側の環境変数設定画面に API KEY 類を移植する。

#### 3. ループ防止

* **[F-01] Bot ID フィルタリングの厳格化**
* `event.get("bot_id")` が存在する場合は、即座に `return` する処理を徹底する。

