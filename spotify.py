import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SCOPE = "user-read-currently-playing user-read-playback-state user-read-recently-played"

def get_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback"),
            scope=SCOPE,
            cache_path=".spotifycache"
        )
    )

sp = get_spotify_client()

def get_current_song_features():
    try:
        current = sp.current_playback()
        track = None
        status = "current"

        if current and current.get("item"):
            track = current["item"]
            if not current.get("is_playing"):
                status = "previous"
        else:
            recent = sp.current_user_recently_played(limit=1)
            if recent["items"]:
                track = recent["items"][0]["track"]
                status = "previous"
            else:
                return None

        info = {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "status": status,
        }

        try:
            features = sp.audio_features(track["id"])
            if features and features[0]:
                f = features[0]
                info.update({
                    "valence": f["valence"],
                    "energy": f["energy"],
                    "tempo": f["tempo"],
                    "danceability": f["danceability"]
                })
        except Exception:
            pass  # free accounts 

        return info

    except Exception as e:
        print("Spotify error:", e)
        return None
