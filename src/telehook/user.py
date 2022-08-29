from typing import Union


class User:
    def __init__(self, payload: dict):
        self.id: int = payload.get('id')
        self.bot: bool = payload.get('is_bot')
        self.first_name: str = payload.get('first_name')
        self.last_name: str = payload.get('last_name')
        self.username: str = payload.get('username')
        self.language: str = payload.get('language_code')
        self.premium: bool = payload.get('is_premium', False)
        self.use_attachment_menu: bool = payload.get('added_to_attachment_menu', False)
