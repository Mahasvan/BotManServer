import aiohttp

session = aiohttp.ClientSession()


async def get_text(url: str, **kwargs):
    async with session.get(url, **kwargs) as response:
        response = (await response.content.read()).decode('utf-8')
    return response


async def get_binary(url: str, **kwargs):
    async with session.get(url, **kwargs) as response:
        response = (await response.content.read())
    return response


async def get_json(url: str, **kwargs):
    async with session.get(url, **kwargs) as response:
        if (await response.text()).lower() == "internal server error":
            return {"response": "Internal Server Error"}
        response = (await response.json())
    return response


async def post(url: str, data: dict = None, params: dict = None):
    async with session.post(url, data=data, params=params) as response:
        response = (await response.content.read()).decode('utf-8')
    return response


async def post_binary(url: str, data: dict = None, params: dict = None):
    async with session.post(url, data=data, params=params) as response:
        response = (await response.content.read())
    return response


async def post_json(url: str, headers: dict = None, data: dict = None, params: dict = None):
    async with session.post(url, headers=headers, data=data, params=params) as response:
        if (await response.text()).lower() == "internal server error":
            return {"response": "Internal Server Error"}
        response = (await response.json())
    return response
