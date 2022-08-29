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

fastapi_app = FastAPI()
fastapi_app.commands = {}
fastapi_app.bot_prefix = None
fastapi_app.bot_signature = None
fastapi_app.telegram_token = None


@fastapi_app.post('/')
async def listener(request: fastapi.Request):
    try:
        signature = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if signature == fastapi_app.bot_signature:
            ctx = Context(await request.json(), token=fastapi_app.telegram_token)
            if ctx.message and ctx.message.text:
                if ctx.message.text.startswith(fastapi_app.bot_prefix):

                    parsed = ctx.message.text.split(" ")
                    command = fastapi_app.commands.get(parsed[0], None)
                    if command:
                        spec = inspect.getfullargspec(command)
                        args = parsed[1:][:len(spec.args)-1]
                        args.insert(0, ctx)  # type: ignore
                        if spec.kwonlyargs:
                            parsed_kwargs = parsed[len(spec.args):]
                            kwargs = {spec.kwonlyargs[0]: " ".join(parsed_kwargs)}
                        else:
                            kwargs = {}
                        if len(args) == len(spec.args):
                            await command(*args, **kwargs)
                            return JSONResponse({"command": parsed[0], " status": "success"}, status_code=200)
                        else:
                            return JSONResponse(
                                {"command": parsed[0], "status": "failed", "reason": "InsufficientArguments"},
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
        fastapi_app.bot_prefix = prefix
        if not token:
            raise ValueError("token value must be given")
        fastapi_app.bot_signature = token.split(":")[-1]
        self.token = token
        fastapi_app.telegram_token = token

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
                fastapi_app.commands[f"{self.prefix}{name or func.__name__}"] = func
                return self
            return wrapper()
        return decorator

    def asgi_app(self, webhook_url: str, ):
        path = "https://api.telegram.org/bot" + self.token + "/setWebhook"
        json_params = {
            "url": webhook_url,
            "secret_token": fastapi_app.bot_signature,
            "drop_pending_updates": True,
            "max_connections": 100
        }
        requests.get(path, json_params)
        return fastapi_app
