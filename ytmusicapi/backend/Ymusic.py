from fastapi import APIRouter, HTTPException, Query
from core_state import HeaderState
from ytmusicapi import YTMusic

router = APIRouter(prefix="/ymusic", tags=["YouTube Music"])


# Utilidad: crear el cliente con los headers del singleton
def get_client():
    state = HeaderState.get_instance()
    headers = state.get_headers()

    if not headers:
        raise HTTPException(status_code=400, detail="Headers no disponibles")

    return YTMusic(headers)


# ---------------------------------------------------------
# 1) GET /ymusic/playlists
# ---------------------------------------------------------
@router.get("/playlists")
def get_playlists():
    yt = get_client()
    playlists = yt.get_library_playlists()

    result = [
        {
            "id": p.get("playlistId"),
            "title": p.get("title"),
            "count": p.get("count")
        }
        for p in playlists
    ]

    return result


# ---------------------------------------------------------
# 2) GET /ymusic/playlist/{playlist_id}
# ---------------------------------------------------------
@router.get("/playlist/{playlist_id}")
def get_playlist_content(playlist_id: str):
    yt = get_client()
    data = yt.get_playlist(playlist_id)

    if not data:
        raise HTTPException(status_code=404, detail="Playlist no encontrada")

    tracks = []
    for t in data.get("tracks", []):
        tracks.append({
            "ytid": t.get("videoId"),
            "title": t.get("title"),
            "artist": t.get("artists", [{}])[0].get("name", "Desconocido"),
            "duration": t.get("duration"),
        })

    return {
        "id": playlist_id,
        "title": data.get("title"),
        "tracks": tracks
    }


# ---------------------------------------------------------
# 3) GET /ymusic/search?q=
# ---------------------------------------------------------
@router.get("/search")
def search_track(q: str = Query(..., min_length=2)):
    yt = get_client()
    results = yt.search(q, filter="songs")

    parsed = []
    for r in results:
        parsed.append({
            "ytid": r.get("videoId"),
            "title": r.get("title"),
            "artist": r.get("artists", [{}])[0].get("name", "Desconocido"),
            "duration": r.get("duration")
        })

    return parsed
