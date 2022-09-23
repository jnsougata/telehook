import asyncio
import inspect
import traceback
from fastapi import FastAPI
from fastapi.requests import Request
from .context import Context, dispatches
from fastapi.responses import JSONResponse


async def handler(request: Request):
    app = request.app
    def check_prefix(text: str) -> bool:
        return text.startswith(app.prefix) or text.startswith(f"@{app.user.username} ")
    try:
        signature = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")

        if signature != app.signature:
            return JSONResponse({"error": "invalid signature"}, status_code=403)

        ctx = Context(await request.json(), token=app.token)

        if ctx.type is not dispatches.unknown:
            listener = app.listeners.get(ctx.type.value, None)
            if listener:
                asyncio.create_task(listener(ctx.message))

        if not (ctx.message and ctx.message.text):
            return JSONResponse({"status": "denied", "reason": "NotTextCommand"}, status_code=401)

        if not check_prefix(ctx.message.text):
            return JSONResponse({"status": "ignored", "reason": "NonCommand"}, status_code=200)

        qualified_text = ctx.message.text.replace(f"@{app.user.username} ", "/")
        parsed = qualified_text.split(" ")
        command = app.commands.get(parsed[0], None)

        if not command:
                return JSONResponse(
                {"command": parsed[0], "status": "ignored", "reason": "NotImplemented"}, status_code=205)

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
    except Exception as e:
        stack = traceback.format_exception(type(e), e, e.__traceback__)
        return JSONResponse({"status": "errored", "reason": " ".join(stack)}, status_code=500)
