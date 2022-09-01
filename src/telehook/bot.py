import re
import inspect
import requests
import asyncio
from .user import User
from .interface import app
from fastapi import FastAPI
from functools import wraps
from typing import Optional, Callable, Any, Tuple


class Bot:

    def __init__(self, token: str, *, prefix: Optional[str] = "/"):
        self.prefix = prefix
        app.bot_prefix = prefix
        if not re.fullmatch("[0-9]+:.*", token):
            raise ValueError("invalid bot token.token should match following regex ([0-9]+:.*)")
        app.bot_signature = token.split(":")[-1]
        self.token = token
        app.telegram_token = token

    def command(self, name: Optional[str] = None):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not asyncio.iscoroutinefunction(func):
                    raise ValueError(f"command <{func.__name__}> must be a coroutine")
                spec = inspect.getfullargspec(func)
                if not spec.args:
                    raise ValueError(f"command <{func.__name__}> must have a single arg")
                if len(spec.kwonlyargs) > 1:
                    raise ValueError(f"command <{func.__name__}> should have only one kwarg")
                if spec.varkw:
                    raise ValueError(f"command <{func.__name__}> should only have positional arguments")
                if spec.defaults:
                    raise ValueError(f"command <{func.__name__}> args can not have default values")
                if spec.varargs:
                    raise ValueError(f"command <{func.__name__}> should only have positional arguments")
                app.commands[f"{self.prefix}{name or func.__name__}"] = func
                return func
            return wrapper()
        return decorator

    @staticmethod
    def on_update(coro: Callable):
        if not asyncio.iscoroutinefunction(coro):
            raise ValueError(f"update listener `{coro.__name__} must be a coroutine function`")
        app.listeners[coro.__name__] = coro

    def router(
            self,
            webhook_host: Optional[str] = None,
            *,
            on_startup: Optional[Callable] = None,
            parameters: Optional[Tuple] = None,
            **kwargs
    ) -> FastAPI:
        try:
            path = f"https://api.telegram.org/bot{self.token}"
            json_params = {
                "url": webhook_host,
                "max_connections": 100,
                "drop_pending_updates": True,
                "secret_token": app.bot_signature,
            }
            requests.get(path + "/setWebhook", json=json_params)
            data = requests.get(path + "/getMe").json()
            app.user = User(**data["result"])
            print(app.user.username)
            on_startup(*parameters, **kwargs)
        finally:
            return app
