import os
import platform
import signal
import socket
import subprocess
import time

try:
    import psutil

    psutil.cpu_percent()
    psutil.virtual_memory().percent
except:
    # todo: implement error logging
    # in some niche systems such as Android+Termux, psutil may not have permissions to view system info
    import api.service.dummy_psutil as psutil

from fastapi import APIRouter

from api.service.routing import RedirectResponse
from api.service import time_assets, system
from api.service.pretty_response import PrettyJSONResponse

router = APIRouter()
router.root_path = None  # populated during setup

prefix = "/host"

start_time = time.time()  # we use this for uptime


@router.get("/")
async def index():
    response = RedirectResponse(url=f"{prefix}/info", root_path=router.root_path)
    return response


@router.get("/info/")
async def hostinfo():
    response = {
        "os": platform.system(),
        "hostname": socket.gethostname(),
        "cpu": system.get_processor_name(),
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


@router.get("/update/")
async def update():
    output = subprocess.check_output("git rev-parse --is-inside-work-tree", shell=True).decode("utf-8")
    if output != "true\n":
        return PrettyJSONResponse(content={"response": "Not a git repository"}, status_code=400)
    output = subprocess.check_output("git pull", shell=True).decode("utf-8")
    response = {
        "response": output
    }
    return PrettyJSONResponse(response)


@router.get("/shutdown/")
async def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    # todo: make startup script shut down existing server instance before starting up a new one
    return PrettyJSONResponse(content={"response": "Somehow I did not shut down."})


def setup(app):
    app.include_router(router, prefix=prefix)
    router.root_path = app.root_path
