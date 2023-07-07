import json
import re

import spotipy
from fastapi import APIRouter
from spotipy.oauth2 import SpotifyClientCredentials

from api.service.pretty_response import PrettyJSONResponse

router = APIRouter()
prefix = "/spotify"

search_router = APIRouter()
search_prefix = "/search"

with open("config.json") as f:
    config = json.load(f)

client_id = config.get("spotify-client-id")
client_secret = config.get("spotify-client-secret")

try:
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                                    client_secret=client_secret))
except spotipy.SpotifyOauthError:
    print("Spotify credentials invalid! Please check your credentials and try again.")

track_id_regex = re.compile(r"(?<=/track/)([a-zA-Z0-9]*?)(?=\?|$0|>)")
playlist_id_regex = re.compile(r"(?<=/playlist/)([a-zA-Z0-9]*?)(?=\?|$0|>)")
album_id_regex = re.compile(r"(?<=/album/)([a-zA-Z0-9]*?)(?=\?|$0|>)")
artist_id_regex = re.compile(r"(?<=/artist/)([a-zA-Z0-9]*?)(?=\?|$0|>)")


@router.get("/track")
async def get_track(track_url: str = None, track_id: str = None):
    if track_url is None and track_id is None:
        response = {
            "response": "Please provide either a track URL or a track ID."
        }
        return PrettyJSONResponse(response)

    if not track_id:
        track_id = track_id_regex.search(track_url).group(1)

    track = spotify.track(track_id)
    return PrettyJSONResponse({"response": track})


@router.get("/album")
async def get_album(album_url: str = None, album_id: str = None):
    if album_url is None and album_id is None:
        response = {
            "response": "Please provide either an album URL or an album ID."
        }
        return PrettyJSONResponse(response)

    if not album_id:
        album_id = album_id_regex.search(album_url).group(1)

    album = spotify.album(album_id)
    return PrettyJSONResponse({"response": album})


@router.get("/artist")
async def get_artist(artist_url: str = None, artist_id: str = None):
    if artist_url is None and artist_id is None:
        response = {
            "response": "Please provide either an artist URL or an artist ID."
        }
        return PrettyJSONResponse(response)

    if not artist_id:
        artist_id = artist_id_regex.search(artist_url).group(1)

    artist = spotify.artist(artist_id)
    return PrettyJSONResponse({"response": artist})


@router.get("/playlist")
async def get_playlist(playlist_url: str = None, playlist_id: str = None):
    if playlist_url is None and playlist_id is None:
        response = {
            "response": "Please provide either a playlist URL or a playlist ID."
        }
        return PrettyJSONResponse(response)

    if not playlist_id:
        playlist_id = playlist_id_regex.search(playlist_url).group(1)

    playlist = spotify.playlist(playlist_id)
    return PrettyJSONResponse({"response": playlist})


@search_router.get("/track")
async def search_track(query: str):
    result = spotify.search(q=query, type="track")
    return PrettyJSONResponse({"response": result})


@search_router.get("/album")
async def search_album(query: str):
    result = spotify.search(q=query, type="album")
    return PrettyJSONResponse({"response": result})


@search_router.get("/artist")
async def search_artist(query: str):
    result = spotify.search(q=query, type="artist")
    return PrettyJSONResponse({"response": result})


@search_router.get("/playlist")
async def search_playlist(query: str):
    result = spotify.search(q=query, type="playlist")
    return PrettyJSONResponse({"response": result})


def setup(app):
    # include the /search router into the /spotify router
    router.include_router(search_router, prefix=search_prefix)

    try:
        app.include_router(router, prefix=prefix)
    except ValueError as e:
        print(e)
        pass
