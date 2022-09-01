import asyncio
import fastapi
import inspect
import traceback
from fastapi import FastAPI
from .context import Context, dispatches
from fastapi.responses import JSONResponse


app = FastAPI()
app.user = None
app.commands = {}
app.listeners = {}
app.bot_prefix = None
app.bot_signature = None
app.telegram_token = None


@app.post('/')
async def handler(request: fastapi.Request):
    def check_prefix(text: str) -> bool:
        return text.startswith(app.bot_prefix) or text.startswith(f"@{app.user.username} ")
    try:
        signature = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if signature == app.bot_signature:
            ctx = Context(await request.json(), token=app.telegram_token)
            if ctx.type is not dispatches.unknown:
                listener = app.listeners.get(ctx.type.value, None)
                if listener:
                    asyncio.create_task(listener(ctx.message))
            if ctx.message and ctx.message.text:
                if check_prefix(ctx.message.text):
                    qualified_text = ctx.message.text.replace(f"@{app.user.username} ", "/")
                    parsed = qualified_text.split(" ")
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
        return JSONResponse({"status": "errored", "reason": " ".join(stack)}, status_code=500)
