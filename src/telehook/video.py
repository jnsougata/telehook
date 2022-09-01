from typing import Optional
from .photosize import PhotoSize


class Video:

    def __init__(self, payload: dict):
        self._payload = payload
        self.file_id: str = payload['file_id']
        self.file_unique_id: str = payload['file_unique_id']
        self.width: int = payload['width']
        self.height: int = payload['height']
        self.duration: int = payload['duration']
        self.file_name: Optional[str] = None
        self.mime_type: Optional[str] = None
        self.file_size: Optional[int] = None

    @property
    def thumb(self) -> Optional[PhotoSize]:
        thumbnail = self._payload.get('thumb')
        if thumbnail:
            return PhotoSize(**thumbnail)
