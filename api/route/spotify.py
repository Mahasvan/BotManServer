import re
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from fastapi import APIRouter

from api.service.pretty_response import PrettyJSONResponse

router = APIRouter()
prefix = "/spotify"

with open("config.json") as f:
    config = json.load(f)

client_id = config.get("spotify-client-id")
client_secret = config.get("spotify-client-secret")

try:
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                                    client_secret=client_secret))
except spotipy.SpotifyOauthError:
    print("Spotify credentials invalid! Please check your credentials and try again.")

track_id_regex = re.compile(r"(?<=\/track\/)([a-zA-Z0-9]*?)(?=\?|$0|\>)")
playlist_id_regex = re.compile(r"(?<=\/playlist\/)([a-zA-Z0-9]*?)(?=\?|$0|\>)")
album_id_regex = re.compile(r"(?<=\/album\/)([a-zA-Z0-9]*?)(?=\?|$0|\>)")
artist_id_regex = re.compile(r"(?<=\/artist\/)([a-zA-Z0-9]*?)(?=\?|$0|\>)")


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


def setup(app):
    try:
        app.include_router(router, prefix=prefix)
    except ValueError as e:
        print(e)
        pass
