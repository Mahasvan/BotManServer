import os
import platform
import socket

# from flask import Blueprint, jsonify, redirect, url_for
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse, RedirectResponse
import psutil

router = APIRouter()
prefix = "/host"


@router.get("/")
async def index():
    response = RedirectResponse(url=f"{prefix}/info")
    return response


@router.get("/info/")
async def hostinfo():
    response = {
        "os": platform.system(),
        "hostname": socket.gethostname(),
        "cpu_threads": os.cpu_count(),
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
    }
    return JSONResponse(content=response)
