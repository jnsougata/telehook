from typing import Union
from .user import User
from .chat import Chat


class Message:
    def __init__(self, payload: dict):
        self.__payload = payload
        self.id = payload['message_id']
        self.date = payload['date']

    @property
    def chat(self) -> Chat:
        return Chat(self.__payload['chat'])

    @property
    def sender_chat(self) -> Chat:
        payload = self.__payload.get('sender_chat')
        if payload:
            return Chat(payload)

    @property
    def via_bot(self) -> bool:
        return self.__payload.get('via_bot', False)

    @property
    def forwarded_by(self) -> User:
        payload = self.__payload.get('forward_from', None)
        if payload:
            return User(payload)

    @property
    def forwarded_from(self) -> Chat:
        payload = self.__payload.get('forward_from_chat', None)
        if payload:
            return Chat(payload)

    @property
    def text(self) -> str:
        return self.__payload.get('text')

    @property
    def author(self) -> User:
        payload = self.__payload.get('from')
        if payload:
            return User(payload)
