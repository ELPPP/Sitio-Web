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
    return RedirectResponse(url)

###metodo callback (el que llama spotify para redirigir el client secret)
@router.get("/auth/spotify/callback")
def callback_spotify(code: str):
    token_data = exchange_code_for_token(code)
    return {"access_token": token_data["access_token"]}

###metodo de intercambio de codigo por token
def exchange_code_for_token(code: str):
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)
    response.raise_for_status()  # lanza error si la respuesta es 4xx/5xx
    return response.json()
