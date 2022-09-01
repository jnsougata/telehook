from typing import Union, Optional, List, Any
from .user import User
from .chat import Chat
from .animation import Animation
from .audio import Audio
from .document import Document
from .photosize import PhotoSize
from .video import Video
from .videonote import VideoNote
from .voice import Voice
from .entity import MessageEntity


class Message:
    def __init__(self, payload: dict):
        self._payload = payload
        self.id = payload['message_id']
        self.date = payload['date']
        self.chat = Chat(self._payload['chat'])
        self.text: Optional[str] = self._payload.get('text')
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
            return User(**payload)

    @property
    def forwarded_from(self) -> Optional[Chat]:
        payload = self._payload.get('forward_from_chat', None)
        if payload:
            return Chat(payload)

    @property
    def author(self) -> Optional[User]:
        payload = self._payload.get('from')
        if payload:
            return User(**payload)

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
    def entities(self) -> Optional[List[MessageEntity]]:
        payload = self._payload.get('entities')
        if payload:
            return [MessageEntity(entity) for entity in payload]

    @property
    def animation(self) -> Optional[Animation]:
        anim = self._payload.get('animation')
        if anim:
            return Animation(anim)

    @property
    def audio(self) -> Optional[Audio]:
        audio = self._payload.get('audio')
        if audio:
            return Audio(audio)

    @property
    def document(self) -> Optional[Document]:
        doc = self._payload.get('document')
        if doc:
            return Document(doc)

    @property
    def photo(self) -> Optional[List[PhotoSize]]:
        photos = self._payload.get('photo')
        if photos:
            return [PhotoSize(**p) for p in photos]

    @property
    def sticker(self) -> Optional[Any]:
        # TODO: create new type
        return self._payload.get('sticker')

    @property
    def video(self) -> Optional[Video]:
        vid = self._payload.get('video')
        if vid:
            return Video(vid)

    @property
    def video_note(self) -> Optional[VideoNote]:
        vid = self._payload.get('video_note')
        if vid:
            return VideoNote(vid)

    @property
    def voice(self) -> Optional[Voice]:
        voice = self._payload.get('voice')
        if voice:
            return Voice(**voice)

    @property
    def caption_entities(self) -> Optional[List[MessageEntity]]:
        payload = self._payload.get('caption_entities')
        if payload:
            return [MessageEntity(entity) for entity in payload]

    # TODO: more
