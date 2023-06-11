from fastapi import APIRouter, Response, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
import googletrans

router = APIRouter()

translator = googletrans.Translator()
lang_dict = googletrans.LANGUAGES
lang_code_dict = googletrans.LANGCODES
lang_list = list(googletrans.LANGUAGES.keys())


@router.post("/")
def index():
    response = RedirectResponse(url="/translate")
    return response


@router.post("/translate/")
async def translate_text(request: Request):
    data = await request.json()
    text = data.get("text")
    src = data.get("src")
    dest = data.get("dest")

    if src != "auto" and src not in lang_list:
        raise HTTPException(status_code=400, detail="Invalid source language")
    if dest not in lang_list and dest != "en":
        raise HTTPException(status_code=400, detail="Invalid destination language")

    response = translator.translate(text, src=src, dest=dest)
    return JSONResponse(content={"response": response.text})


@router.get("/languages/")
def languages():
    return JSONResponse(content={"response": lang_dict})


@router.post("/detect/")
async def detect(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    result = translator.detect(text)
    lang_name = result.lang
    lang_confidence = result.confidence * 100
    print(lang_confidence)
    print(lang_name)

    if isinstance(result.confidence, list):
        # sometimes the result may contain two or more language detections
        # no idea why, but we'll just take the first one
        lang_confidence = result.confidence[0]
        lang_name = result.lang[0]

    response = {
        "response": {
            "langcode": lang_name,
            "language": lang_dict.get(lang_name),
            "confidence": lang_confidence
        }
    }
    return JSONResponse(content=response)


@router.post("/pronounce/")
async def pronounce(request: Request):
    data = await request.json()
    text = data.get("text")
    lang = data.get("lang")

    if not lang:
        tempresult = translator.detect(text)
        lang = tempresult.lang
        if isinstance(tempresult.lang, list):
            lang = tempresult.lang[0]

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    if lang not in lang_list:
        raise HTTPException(status_code=400, detail="Invalid language")

    result = translator.translate(text, src=lang, dest=lang)
    response = {
        "response": {
            "text": text,
            "pronunciation": result.pronunciation,
            "langcode": lang,
            "language": lang_dict.get(lang)
        }
    }
    return JSONResponse(content=response)
