from typing import Optional
from .user import User


class MessageEntity:

    def __init__(self, payload: dict):
        self._payload = payload
        self.type = payload['type']
        self.offset = payload['offset']
        self.length = payload['length']
        self.url: Optional[str] = payload.get('url')
        self.language: Optional[str] = payload.get('language')
        self.custom_emoji_id: Optional[str] = payload.get('custom_emoji_id')

    @property
    def user(self) -> Optional[User]:
        payload = self._payload.get('user')
        if payload:
            return User(**payload)
