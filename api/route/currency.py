import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from api.service import internet
from api.service.pretty_response import PrettyJSONResponse

router = APIRouter()
prefix = "/currency"

with open("config.json") as f:
    config = json.load(f)

currency_api_key = config.get("currency-api-key")
rates = {}


async def update_rates():
    global rates
    rates = await internet.get_json(f"https://free.currconv.com/api/v7/currencies?apiKey={currency_api_key}")


if currency_api_key is not None:
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(update_rates())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        loop.create_task(update_rates())
        loop.close()

if rates.get("status") == 400:
    print(rates.get("error"))
    # todo: send this to error logger whenever it is implemented
    rates = {}


@router.get("/")
async def index():
    return RedirectResponse(f"{prefix}/rates")


@router.get("/rates/")
async def exchange_rates():
    return PrettyJSONResponse({"response": rates})


@router.get("/convert/")
async def convert(currency_from: str, currency_to: str, amount: float):
    result = await internet.get_json(f"https://free.currconv.com/api/v7/convert?q="
                                     f"{currency_from}_{currency_to}&compact=ultra&apiKey={currency_api_key}")
    if result == {}:
        response = {
            "response": "Could not fetch results. Please check the currency codes."
        }
        return PrettyJSONResponse(response, 400)
    else:
        try:
            from_currency, to_currency = [x.upper() for x in list(result.keys())[0].split("_")]
        except ValueError:
            # api is down
            response = {
                "response": "could not retrieve exchange rates"
            }
            return PrettyJSONResponse(response, 500)
        multiplier = list(result.values())[0]
        response = {
            "response": {
                "from": from_currency,
                "to": to_currency,
                "amount": amount * multiplier
            }
        }
        return PrettyJSONResponse(response)


def setup(app):
    app.include_router(router, prefix=prefix)
