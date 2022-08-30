from typing import Union, Optional, List, Any
from .user import User
from .chat import Chat


class Message:
    def __init__(self, payload: dict):
        self._payload = payload
        self.id = payload['message_id']
        self.date = payload['date']
        self.chat = Chat(self._payload['chat'])
        self.text: Optional[str] = self._payload['text']
        self.caption: Optional[str] = self._payload.get('caption')

    @property
    def sender_chat(self) -> Optional[Chat]:
        payload = self._payload.get('sender_chat')
        if payload:
            return Chat(payload)

    @property
    def via_bot(self) -> bool:
        return self._payload.get('via_bot', False)

    @property
    def forwarded_by(self) -> Optional[User]:
        payload = self._payload.get('forward_from', None)
        if payload:
            return User(payload)

    @property
    def forwarded_from(self) -> Optional[Chat]:
        payload = self._payload.get('forward_from_chat', None)
        if payload:
            return Chat(payload)

    @property
    def author(self) -> Optional[User]:
        payload = self._payload.get('from')
        if payload:
            return User(payload)

    @property
    def edited_date(self) -> Optional[int]:
        return self._payload.get('edit_date')

    @property
    def has_protected_content(self) -> bool:
        return self._payload.get('has_protected_content', False)

    @property
    def media_group_id(self) -> Optional[str]:
        return self._payload.get('media_group_id')

    @property
    def author_signature(self) -> Optional[str]:
        return self._payload.get('author_signature')

    @property
    def entities(self) -> Optional[List[Any]]:
        # TODO: create new type
        return self._payload.get('entities')

    @property
    def animation(self) -> Optional[Any]:
        # TODO: create new type
        return self._payload.get('animation')

    @property
    def audio(self) -> Optional[Any]:
        # TODO: create new type
        return self._payload.get('audio')

    @property
    def document(self) -> Optional[Any]:
        # TODO: create new type
        return self._payload.get('document')

    @property
    def photo(self) -> Optional[List[Any]]:
        # TODO: create new type
        return self._payload.get('photo')

    @property
    def sticker(self) -> Optional[Any]:
        # TODO: create new type
        return self._payload.get('sticker')

    @property
    def video(self) -> Optional[Any]:
        # TODO: create new type
        return self._payload.get('video')

    @property
    def video_note(self) -> Optional[Any]:
        return self._payload.get('video_note')

    @property
    def voice(self) -> Optional[Any]:
        # TODO: create new type
        return self._payload.get('voice')

    @property
    def caption_entities(self) -> Optional[List[Any]]:
        # TODO: create type
        return self._payload.get('caption_entities')

    # TODO: more
