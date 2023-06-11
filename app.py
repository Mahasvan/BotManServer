import json, importlib
import importlib.util

from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse

from api.route.translate import router
from api.route.host import router

app = FastAPI()


@app.get('/')
async def index():
    response = RedirectResponse(url='/ping')
    return response


@app.get('/ping/')
async def ping():
    response = {"response": "I am alive!"}
    return JSONResponse(content=response)


@app.get('/urls/')
async def urls():
    return JSONResponse(content=app.openapi())

with open("api/route/routes.json") as f:
    routes = json.load(f)

for route in routes:
    importlib.util.spec_from_file_location(route["file"], f"api/route/{route['file']}.py")
    module = importlib.import_module(f"api.route.{route['file']}")
    app.include_router(module.router, prefix=route["prefix"])

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
