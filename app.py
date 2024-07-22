import importlib.util
import json
import os

import requests
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.service import error_handler
from api.service.pretty_response import PrettyJSONResponse

error_handler.set_exception_handler()

with open("config.json") as f:
    config = json.load(f)
    os.environ['LOGFILE_PATH'] = config.get("logfile", "log.db")


def close_running_instance():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((config.get("host"), config.get("port")))
    except socket.error:
        print("Port is already in use. Shutting down running instance...")

        try:
            requests.get(f"http://{config.get('host')}:{config.get('port')}/host/shutdown")
        except requests.exceptions.ConnectionError:
            print("Could not connect to running instance. Assuming it is already shut down...")
        else:
            print("Closed running instance.")


close_running_instance()

root_path = os.environ.get("FASTAPI_ROOT_PATH", None)
if root_path:
    print(f"Using root path: {root_path}")
    app = FastAPI(root_path=root_path)
else:
    app = FastAPI()


@app.get('/')
async def index():
    response = RedirectResponse(url='/ping')
    return response


@app.get('/ping/')
async def ping():
    response = {"response": "I am alive!"}
    return PrettyJSONResponse(content=response)


@app.get('/urls/')
async def urls():
    response = {"response": app.openapi().get("paths")}
    return PrettyJSONResponse(response)


with open("api/route/routes.json") as f:
    routes = json.load(f)

for route in routes:
    importlib.util.spec_from_file_location(route, f"api/route/{route}.py")
    module = importlib.import_module(f"api.route.{route}")
    module.setup(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host=config.get("host"), port=config.get("port"))
