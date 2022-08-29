from enum import Enum


class ChatTypes(Enum):
    private = "private"
    group = "group"
    super_group = "supergroup"
    channel = "channel"


class Chat:
    def __init__(self, payload: dict):
        self.__payload = payload
        self.id = payload['id']
        self.type = ChatTypes(payload['type'])
        self.title = payload.get('title', None)
        self.username = payload.get('username', None)
        self.first_name = payload.get('first_name', None)
        self.last_name = payload.get('last_name', None)
        # self.photo = payload.get('photo', None)
        # self.bio = payload.get('bio', None)
        # TODO: more fields
