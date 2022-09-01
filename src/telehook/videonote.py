from typing import Union, Optional
from .photosize import PhotoSize


class VideoNote:

    def __init__(self, payload: dict):
        self._payload = payload
        self.file_id: str = payload['file_id']
        self.file_unique_id: str = payload['file_unique_id']
        self.length: int = payload['length']
        self.duration: int = payload['duration']
        self.file_size: Optional[int] = payload.get('file_size')

    @property
    def thumb(self) -> Optional[PhotoSize]:
        thumbnail = self._payload.get('thumb')
        if thumbnail:
            return PhotoSize(**thumbnail)
