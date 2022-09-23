import re
import hashlib
import inspect
import requests
from .user import User
from .interface import app
from fastapi import FastAPI
from functools import wraps
from .interface import handler
from typing import Optional, Callable, Any, Tuple


def _match_token(token: str) -> bool:
    return re.fullmatch("[0-9]+:.*", token)

def _create_signature(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class Bot(FastAPI):

    def __init__(self, token: str, *, prefix: Optional[str] = "/"):
        super().__init__()
        self.prefix = prefix
        self.commands = {}
        self.listeners = {}
        self.user: User = None
        assert _match_token(token), "invalid token"
        self.token = token
        self.signature = _create_signature(token.split(":")[-1])
        self.add_route("/", handler, methods=["POST"])

    def command(self, name: Optional[str] = None):

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not inspect.iscoroutinefunction(func):
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
                self.commands[f"{self.prefix}{name or func.__name__}"] = func
                return func
            return wrapper()
        return decorator

    def on_update(self, coro: Callable):
        if not inspect.iscoroutinefunction(coro):
            raise ValueError(f"update listener `{coro.__name__} must be a coroutine function`")
        self.listeners[coro.__name__] = coro

    def export(
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
                "secret_token": self.signature,
            }
            requests.get(path + "/setWebhook", json=json_params)
            data = requests.get(path + "/getMe").json()
            self.user = User(**data["result"])
            print(self.user.username)
            on_startup(*parameters, **kwargs)
        finally:
            return app
