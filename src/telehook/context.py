from typing import Union
import requests
from enum import Enum
from .message import Message


def encode(string: str) -> str:
    forbidden = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in forbidden:
        if char in string:
            text = string.replace(char, f'\\{char}')
        return string


class Dispatch(Enum):
    dm_message = "message"
    dm_edit = "edited_message"
    channel_message = "channel_post"
    channel_message_edit = "edited_channel_post"
    unknown = "_"


class Context:
    __ROOT_URL = "https://api.telegram.org/bot"

    def __init__(self, payload: dict, *, token: str):
        self.__payload = payload
        if Dispatch.dm_message.value in self.__payload:
            self.type = Dispatch.dm_message
        elif Dispatch.dm_edit.value in self.__payload:
            self.type = Dispatch.dm_edit
        elif Dispatch.channel_message.value in self.__payload:
            self.type = Dispatch.channel_message
        elif Dispatch.channel_message_edit.value in self.__payload:
            self.type = Dispatch.channel_message_edit
        else:
            self.type = Dispatch.unknown
        self.__token = token
        self._data = payload.get(self.type.value)
        self.id = payload['update_id']

    @property
    def message(self) -> Message:
        if self.type is not Dispatch.unknown:
            return Message(self._data)

    async def send(self, text: str, **kwargs):
        path = self.__ROOT_URL + self.__token + f'/sendMessage'
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
