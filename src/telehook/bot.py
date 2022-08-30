import inspect
import logging
import fastapi
import asyncio
import requests
import traceback
from typing import Union
from fastapi import FastAPI
from functools import wraps
from .context import Context
from fastapi.responses import JSONResponse

app = FastAPI()
app.commands = {}
app.bot_prefix = None
app.bot_signature = None
app.telegram_token = None


@app.post('/')
async def handler(request: fastapi.Request):
    try:
        signature = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if signature == app.bot_signature:
            ctx = Context(await request.json(), token=app.telegram_token)
            if ctx.message and ctx.message.text:
                if ctx.message.text.startswith(app.bot_prefix):
                    parsed = ctx.message.text.split(" ")
                    command = app.commands.get(parsed[0], None)
                    if command:
                        spec = inspect.getfullargspec(command)
                        args = parsed[1:][:len(spec.args)-1]
                        args.insert(0, ctx)  # type: ignore
                        parsed_kwargs = parsed[len(spec.args):]
                        if spec.kwonlyargs and not parsed_kwargs:
                            return JSONResponse(
                                {"command": parsed[0], "status": "failed", "reason": "InsufficientKwargs"},
                                status_code=203)
                        elif spec.kwonlyargs:
                            kwargs = {spec.kwonlyargs[0]: " ".join(parsed_kwargs)}
                            if len(args) == len(spec.args):
                                await command(*args, **kwargs)
                                return JSONResponse({"command": parsed[0], " status": "success"}, status_code=200)
                            else:
                                return JSONResponse(
                                    {"command": parsed[0], "status": "failed", "reason": "InsufficientArgs"},
                                    status_code=203)
                        else:
                            if len(args) == len(spec.args):
                                await command(*args)
                                return JSONResponse({"command": parsed[0], " status": "success"}, status_code=200)
                            else:
                                return JSONResponse(
                                    {"command": parsed[0], "status": "failed", "reason": "InsufficientArgs"},
                                    status_code=203)
                    else:
                        return JSONResponse(
                            {"command": parsed[0], "status": "ignored", "reason": "NotImplemented"}, status_code=205)
                else:
                    return JSONResponse({"status": "ignored", "reason": "NonCommand"}, status_code=200)
        else:
            return JSONResponse({"status": "denied", "reason": "Unauthorized"}, status_code=401)
    except Exception as e:
        stack = traceback.format_exception(type(e), e, e.__traceback__)
        return fastapi.responses.PlainTextResponse("".join(stack), status_code=500)


class Bot:

    def __init__(self, token: str, *, prefix: str = "/"):
        self.prefix = prefix
        app.bot_prefix = prefix
        if not token:
            raise ValueError("token value must be given")
        app.bot_signature = token.split(":")[-1]
        self.token = token
        app.telegram_token = token

    def command(self, name: str = None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not asyncio.iscoroutinefunction(func):
                    raise RuntimeError(f"command <{func.__name__}> must be a coroutine")
                spec = inspect.getfullargspec(func)
                if len(spec.kwonlyargs) > 1:
                    raise ValueError(f"command <{func.__name__}> should only one kwarg")
                if spec.varkw:
                    raise ValueError(f"command <{func.__name__}> should only have positional arguments")
                if spec.defaults:
                    raise ValueError(f"command <{func.__name__}> args can not have default values")
                if spec.varargs:
                    raise ValueError(f"command <{func.__name__}> should only have positional arguments")
                app.commands[f"{self.prefix}{name or func.__name__}"] = func
                return self
            return wrapper()
        return decorator

    def gateway(self, webhook_url: str):
        if not webhook_url:
            raise ValueError("webhook_url can not be empty")
        path = "https://api.telegram.org/bot" + self.token + "/setWebhook"
        json_params = {
            "url": webhook_url,
            "max_connections": 100,
            "drop_pending_updates": True,
            "secret_token": app.bot_signature,
        }
        requests.get(path, json=json_params)
        return app
