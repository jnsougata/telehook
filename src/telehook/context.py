from typing import Union
import requests
from .enums import dispatches, try_enum
from .message import Message


def encode(string: str) -> str:
    forbidden = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in forbidden:
        if char in string:
            text = string.replace(char, f'\\{char}')
        return string


def dispatch(data: dict) -> dispatches:
    if dispatches.message.value in data:
        return dispatches.message
    elif dispatches.edited_message.value in data:
        return dispatches.edited_message
    elif dispatches.channel_post.value in data:
        return dispatches.channel_post
    elif dispatches.edited_channel_post.value in data:
        return dispatches.edited_channel_post
    else:
        return dispatches.unknown


class Context:
    _ROOT_URL = "https://api.telegram.org/bot"

    def __init__(self, payload: dict, *, token: str):
        self._payload = payload
        self.type = dispatch(payload)
        self.__token = token
        self._data = payload.get(self.type.value)
        self.id = payload['update_id']

    @property
    def message(self) -> Message:
        if self.type is not dispatches.unknown:
            return Message(self._data)

    async def send(self, text: str, **kwargs):
        path = self._ROOT_URL + self.__token + f'/sendMessage'
        if self.message:
            if self.message.chat.id:
                target = self.message.chat.id
            elif self.message.sender_chat.id:
                target = self.message.sender_chat.id
            else:
                target = None
            payload = {
                "text": encode(text),
                "chat_id": target,
                "parse_mode": 'MarkdownV2'
            }
            requests.get(path, json=payload)
