import json
import os
import re
from typing import Any, Dict

import numpy as np
import pytesseract
from PIL import Image, ExifTags


def is_serializable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False


class ImageProcessor:
    def __init__(self, exec_path: str = "tesseract", tessdata_path: str = None):
        self.exec_path = exec_path
        self.tessdata_path = tessdata_path
        if exec_path:
            pytesseract.pytesseract.tesseract_cmd = exec_path
        if tessdata_path:
            os.environ["TESSDATA_PREFIX"] = tessdata_path
            pytesseract.pytesseract.tessdata_path = tessdata_path

    def read_file(self, file_path) -> Image:
        img_to_ocr = Image.open(file_path)
        return img_to_ocr

    def read_bytes(self, bytes, dimensions: tuple) -> Image:
        img_to_ocr = Image.frombytes("RGB", dimensions, bytes)
        return img_to_ocr

    def detect_ocr_metadata(self, image: Image) -> Dict[str, Any]:

        lang = pytesseract.image_to_osd(image=np.array(image))
        script_regex = r"(?<=Script:\s)(.*)(?=\n)"
        script_confidence_regex = r"(?<=Script confidence:\s)(.*)(?=\n)?"
        orientation_regex = r"(?<=Orientation in degrees:\s)(.*)(?=\n)?"
        orientation_confidence_regex = r"(?<=Orientation confidence:\s)(.*)(?=\n)?"
        script = re.search(script_regex, lang).group(0)
        script_confidence = re.search(script_confidence_regex, lang).group(0)
        orientation = re.search(orientation_regex, lang).group(0)
        orientation_confidence = re.search(orientation_confidence_regex, lang).group(0)

        return {
            "script": script,
            "script_confidence": script_confidence,
            "orientation": orientation,
            "orientation_confidence": orientation_confidence
        }

    def detect_metadata(self, image: Image) -> Dict[str, Any]:
        exif = {ExifTags.TAGS[k]: v for k, v in image.getexif().items() if k in ExifTags.TAGS and is_serializable(v)}
        return exif

    def ocr_image(self, img_to_ocr: np.array, lang: str = None) -> str:
        if lang is None:
            lang = "eng"

        return pytesseract.image_to_string(img_to_ocr, lang=lang)
