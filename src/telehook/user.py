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
        self.enabled_attachment_menu: bool = payload.get('added_to_attachment_menu', False)
        self.can_join_groups: bool = payload.get('can_join_groups', None)
        self.access_group_messages: bool = payload.get('can_read_all_group_messages', None)
        self.supports_inline_queries: bool = payload.get('supports_inline_queries', False)
