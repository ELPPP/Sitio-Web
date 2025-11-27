import os
import requests
from urllib.parse import urlencode
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv


router = APIRouter()
load_dotenv()



#gestion de tokens

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")



###metodo de redireccion (construye el enlace)
@router.get("/auth/spotify/login")
async def login_spotify():
    if not CLIENT_ID or not REDIRECT_URI:
        return {"error": "Faltan variables de entorno. Verifica tu configuración."}
    
    base_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "user-read-private user-read-email",
    }

    # Construcción segura del enlace
    url = f"{base_url}?{urlencode(params)}"
    #return {"redirect_uri": REDIRECT_URI, "final_url": url}
    return RedirectResponse(url)


