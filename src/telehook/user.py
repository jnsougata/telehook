from typing import Union, Optional
from dataclasses import dataclass


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language: Optional[str] = None
    premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = False
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = False
