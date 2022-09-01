from typing import Optional
from .photosize import PhotoSize
from dataclasses import dataclass


@dataclass
class Document:

    def __init__(self, payload: dict):
        self._payload = payload
        self.file_id: str = payload['file_id']
        self.file_unique_id: str = payload['file_unique_id']
        self.file_name: Optional[str] = payload.get('file_name')
        self.mime_type: Optional[str] = payload.get('mime_type')
        self.file_size: Optional[int] = payload.get('file_size')

    @property
    def thumb(self) -> Optional[PhotoSize]:
        thumbnail = self._payload.get('thumb')
        if thumbnail:
            return PhotoSize(**thumbnail)
