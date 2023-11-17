import json
import os
from typing import Annotated, Tuple

from fastapi import APIRouter, File

from api.service.image_processing import ImageProcessor
from api.service.pretty_response import JSONResponse
from api.service.rng import generate_otp


router = APIRouter()
prefix = "/image"

with open("config.json") as f:
    config = json.load(f)
    exec_path = config.get("tesseract_exec_path", None)
    tessdata_path = config.get("tesseract_tessdata_path", None)

ocr = ImageProcessor(exec_path, tessdata_path)

if not os.path.exists("temp"):
    os.mkdir("temp")

@router.post("/ocr-meta")
async def ocr_meta(file: Annotated[bytes, File()], extension: str = "png"):
    filename = os.path.join("temp", f"{generate_otp()}.{extension}")
    with open(filename, "wb") as f:
        f.write(file)
    img_to_ocr = ocr.read_file("temp.png")
    os.remove(filename)
    return JSONResponse(ocr.detect_ocr_metadata(img_to_ocr))


@router.post("/metadata")
async def metadata(file: Annotated[bytes, File()], extension: str = "png"):
    filename = os.path.join("temp", f"{generate_otp()}.{extension}")
    with open(filename, "wb") as f:
        f.write(file)
    img_to_ocr = ocr.read_file("temp.png")
    os.remove(filename)
    return JSONResponse(ocr.detect_metadata(img_to_ocr))


@router.post("/ocr")
async def ocr_image(file: Annotated[bytes, File()], extension: str = "png", language_code: str = "eng"):
    filename = os.path.join("temp", f"{generate_otp()}.{extension}")
    with open(filename, "wb") as f:
        f.write(file)
    img_to_ocr = ocr.read_file("temp.png")
    os.remove(filename)
    return JSONResponse({"text": ocr.ocr_image(img_to_ocr, language_code)})


def setup(app):
    app.include_router(router, prefix=prefix)
