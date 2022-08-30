from enum import Enum


def try_enum(enum_class, value):
    try:
        return enum_class(value)
    except ValueError:
        return


class dispatches(Enum):
    message = "message"
    edited_message = "edited_message"
    channel_post = "channel_post"
    edited_channel_post = "edited_channel_post"
    inline_query = "inline_query"
    chosen_inline_result = "chosen_inline_result"
    callback_query = "callback_query"
    shipping_query = "shipping_query"
    pre_checkout_query = "pre_checkout_query"
    poll = "poll"
    poll_answer = "poll_answer"
    my_chat_member = "my_chat_member"
    chat_member = "chat_member"
    chat_join_request = "chat_join_request"
    unknown = "_"


class chat_types(Enum):
    private = "private"
    group = "group"
    super_group = "supergroup"
    channel = "channel"
