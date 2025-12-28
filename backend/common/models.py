from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class SlackMessage:
    """
    [F-01 〜 F-04用]
    Slackからの入力を管理する共通クラス。
    """
    event_id: str
    user_id: str
    text_content: str
    
    # ▼▼▼ これがエラーの原因でした。ここに追加します ▼▼▼
    channel_id: str
    # ▲▲▲ ---------------------------------------

    source: str = "slack"
    intent_tag: Optional[str] = None
    status: str = "pending"

    @classmethod
    def from_dict(cls, data: dict):
        """辞書形式(JSON)からクラスを生成する"""
        return cls(**data)

    def to_dict(self):
        """クラスを辞書形式(JSON用)に変換する"""
        return asdict(self)


@dataclass
class FeedbackResponse:
    """
    [F-04 〜 F-06用]
    生成されたフィードバックを管理するクラス。
    """
    event_id: str
    target_user_id: str
    feedback_summary: str
    status: str = "complete"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return asdict(self)