from enum import Enum
from .enums import chat_types


class Chat:
    def __init__(self, payload: dict):
        self._payload = payload
        self.id = payload['id']
        self.type = chat_types(payload['type'])
        self.title = payload.get('title', None)
        self.username = payload.get('username', None)
        self.first_name = payload.get('first_name', None)
        self.last_name = payload.get('last_name', None)
        self.photo = payload.get('photo', None)
        self.bio = payload.get('bio', None)
        self.has_private_forwards: bool = payload.get('has_private_forwards', None)
        self.join_to_send_messages: bool = payload.get('join_to_send_messages', None)
        self.join_by_request: bool = payload.get('join_by_request', None)
        self.description = payload.get('description', None)
        self.invite_link = payload.get('invite_link', None)
        self.pinned_message = payload.get('pinned_message', None)
        self.permissions = payload.get('permissions', None)
        self.slow_mode_delay: int = payload.get('slow_mode_delay', 0)
        self.message_auto_delete_time: int = payload.get('message_auto_delete_time', None)
        self.has_protected_content: bool = payload.get('has_protected_content', None)
        self.sticker_set_name: str = payload.get('sticker_set_name', None)
        self.can_set_sticker_set: bool = payload.get('can_set_sticker_set', None)
        self.linked_chat_id: int = payload.get('linked_chat_id', None)
        self.location = payload.get('location', None)
        self.restricted_voice_video: bool = payload.get('has_restricted_voice_and_video_messages')
