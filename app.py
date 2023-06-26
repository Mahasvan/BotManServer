import json
import importlib.util

from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse

from api.service.pretty_response import PrettyJSONResponse
app = FastAPI()

with open("config.json") as f:
    config = json.load(f)

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
    return PrettyJSONResponse(content=app.openapi())


with open("api/route/routes.json") as f:
    routes = json.load(f)

for route in routes:
    importlib.util.spec_from_file_location(route, f"api/route/{route}.py")
    module = importlib.import_module(f"api.route.{route}")
    module.setup(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
