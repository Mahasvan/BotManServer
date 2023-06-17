import os
import platform
import socket
import time

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import psutil

from api.service import time_assets
from api.service.pretty_response import PrettyJSONResponse

router = APIRouter()
prefix = "/host"

start_time = time.time()
# we use this for uptime


@router.get("/")
async def index():
    response = RedirectResponse(url=f"{prefix}/info")
    return response


@router.get("/info/")
async def hostinfo():
    response = {
        "os": platform.system(),
        "hostname": socket.gethostname(),
        "cpu_threads": os.cpu_count(),
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
    }
    return PrettyJSONResponse(content=response)


@router.get("/uptime/")
async def uptime():
    now_time = time.time()
    seconds = now_time - start_time
    pretty_uptime = time_assets.pretty_time_from_seconds(int(seconds))
    response = {
        "response": {
            "seconds": seconds,
            "text": pretty_uptime
        }
    }
    return PrettyJSONResponse(response)


def setup(app):
    app.include_router(router, prefix=prefix)
