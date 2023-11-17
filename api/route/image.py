import os
from typing import Annotated, Tuple

from fastapi import APIRouter, File

from api.service.image_processing import ImageProcessor
from api.service.pretty_response import JSONResponse
from api.service.rng import generate_otp


router = APIRouter()
prefix = "/image"

ocr = ImageProcessor()

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
async def ocr_image(file: Annotated[bytes, File()], extension: str = "png"):
    filename = os.path.join("temp", f"{generate_otp()}.{extension}")
    with open(filename, "wb") as f:
        f.write(file)
    img_to_ocr = ocr.read_file("temp.png")
    os.remove(filename)
    return JSONResponse({"text": ocr.ocr_image(img_to_ocr)})


def setup(app):
    app.include_router(router, prefix=prefix)
