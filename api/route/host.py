import os
import platform
import socket

from flask import Blueprint, jsonify, redirect, url_for
import psutil

host = Blueprint("host", __name__)


@host.route("/")
def index():
    return redirect(url_for("host.info"))


@host.route("/info/")
def hostinfo():
    response = {
        "os": platform.system(),
        "hostname": socket.gethostname(),
        "cpu_threads": os.cpu_count(),
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
    }
    return jsonify(response)
