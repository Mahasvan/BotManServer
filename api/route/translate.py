from flask import Blueprint, jsonify, redirect, url_for, request

import googletrans

translate = Blueprint("translate", __name__)

translator = googletrans.Translator()
lang_dict = googletrans.LANGUAGES
lang_code_dict = googletrans.LANGCODES
lang_list = list(googletrans.LANGUAGES.keys())


@translate.route("/", methods=["POST"])
def index():
    return redirect(url_for("translate.translate_text"))


@translate.route("/translate/", methods=["POST"])
def translate_text():
    """
    :param text: the text to translate
    :param src: source language, use "auto" for auto-detection
    :param dest: destination language, use "en" for English
    :return:
    """
    text = request.get_json().get("text")
    src = request.get_json().get("src")
    dest = request.get_json().get("dest")

    if src != "auto" and src not in lang_list:
        return jsonify({"response": "Invalid source language"}), 400
    if dest not in lang_list and dest != "en":
        return jsonify({"response": "Invalid destination language"}), 400

    response = translator.translate(text, src=src, dest=dest)
    return jsonify({"response": response.text})


@translate.route("/languages/", methods=["GET"])
def languages():
    return jsonify({"response": lang_dict})


@translate.route("/detect/", methods=["POST"])
def detect():
    """
    :param text: the text to detect
    :return:
    """
    text = request.get_json().get("text")
    if not text:
        return jsonify({"response": "No text provided"}), 400

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
    return jsonify(response)


@translate.route("/pronounce/", methods=["POST"])
def pronounce():
    """
    :param text: the text to pronounce
    :param lang: the language to pronounce in
    :return:
    """
    text = request.get_json().get("text")
    lang = request.get_json().get("lang")

    if not lang:
        tempresult = translator.detect(text)
        lang = tempresult.lang
        if isinstance(tempresult.lang, list):
            lang = tempresult.lang[0]

    if not text:
        return jsonify({"response": "No text provided"}), 400
    if lang not in lang_list:
        return jsonify({"response": "Invalid language"}), 400

    result = translator.translate(text, src=lang, dest=lang)
    response = {
        "response": {
            "text": text,
            "pronunciation": result.pronunciation,
            "langcode": lang,
            "language": lang_dict.get(lang)
        }
    }
    return jsonify(response)
