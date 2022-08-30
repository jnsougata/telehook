import inspect
import requests
import asyncio
from .interface import app
from fastapi import FastAPI
from functools import wraps
from typing import Optional, Callable


class Bot:

    def __init__(
            self, token: str,
            *,
            prefix: Optional[str] = "/",
            set_webhook: bool = False
    ):
        self.prefix = prefix
        app.bot_prefix = prefix
        self._auto_set_webhook = set_webhook
        if not token:
            raise ValueError("token value can not be empty")
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

    def gateway(self, webhook_url: Optional[str] = None) -> FastAPI:
        if self._auto_set_webhook:
            if not webhook_url:
                raise RuntimeError("`webhook_url` can not be empty when `set_webhook` is True")
            path = "https://api.telegram.org/bot" + self.token + "/setWebhook"
            json_params = {
                "url": webhook_url,
                "max_connections": 100,
                "drop_pending_updates": True,
                "secret_token": app.bot_signature,
            }
            requests.get(path, json=json_params)
        return app
