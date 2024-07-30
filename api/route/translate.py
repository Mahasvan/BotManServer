import googletrans
from fastapi import APIRouter, Request, HTTPException
from api.service.routing import RedirectResponse

from api.service.pretty_response import PrettyJSONResponse

router = APIRouter()
router.root_path = None # populated during import
prefix = "/translate"

translator = googletrans.Translator()
lang_dict = googletrans.LANGUAGES
lang_code_dict = googletrans.LANGCODES
lang_list = list(googletrans.LANGUAGES.keys())


@router.post("/")
def index():
    response = RedirectResponse(url=prefix, root_path=router.root_path)
    return response


@router.post("/translate/")
async def translate_text(request: Request):
    data = await request.json()
    text = data.get("text")
    src = data.get("src")
    dest = data.get("dest")

    if src != "auto" and src not in lang_list:
        response = {
            "response": "Invalid source language"
        }
        return PrettyJSONResponse(response, 400)
    if dest not in lang_list and dest != "en":
        response = {
            "response": "Invalid destination language"
        }
        return PrettyJSONResponse(response, 400)

    response = await translator.translate(text, src=src, dest=dest)
    return PrettyJSONResponse(content={"response": {
        "text": response.text,
        "src": response.src,
        "dest": response.dest,
    }
    })


@router.get("/languages/")
def languages():
    return PrettyJSONResponse(content={"response": lang_dict})


@router.post("/detect/")
async def detect(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    result = await translator.detect(text)

    if isinstance(result.confidence, list):
        # sometimes the result may contain two or more language detections
        # no idea why, but we'll just take the first one
        lang_confidence = result.confidence[0] * 100
        lang_name = result.lang[0]
    else:
        lang_name = result.lang
        lang_confidence = result.confidence * 100

    response = {
        "response": {
            "langcode": lang_name,
            "language": lang_dict.get(lang_name),
            "confidence": lang_confidence
        }
    }
    return PrettyJSONResponse(content=response)


@router.post("/pronounce/")
async def pronounce(request: Request):
    data = await request.json()
    text = data.get("text")
    lang = data.get("lang")

    if not lang:
        tempresult = await translator.detect(text)
        lang = tempresult.lang
        if isinstance(tempresult.lang, list):
            lang = tempresult.lang[0]

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    if lang not in lang_list:
        raise HTTPException(status_code=400, detail="Invalid language")

    result = await translator.translate(text, src=lang, dest=lang)
    response = {
        "response": {
            "text": text,
            "pronunciation": result.pronunciation,
            "langcode": lang,
            "language": lang_dict.get(lang)
        }
    }
    return PrettyJSONResponse(content=response)


def setup(app):
    app.include_router(router, prefix=prefix)
    router.root_path = app.root_path
