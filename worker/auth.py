import os
import requests
import base64
from urllib.parse import urlencode
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv


router = APIRouter()
load_dotenv()
print("🧪 CLIENT_ID:", os.getenv("SPOTIFY_CLIENT_ID"))
print("🧪 REDIRECT_URI (repr):", repr(os.getenv("SPOTIFY_REDIRECT_URI")))




###metodo callback (el que llama spotify para redirigir el client secret)
@router.get("/auth/spotify/callback")
def callback_spotify(code: str):
    token_data = exchange_code_for_token(code)
    return {"access_token": token_data["access_token"]}

###metodo de intercambio de codigo por token
def exchange_code_for_token(code: str):
    token_url = "https://accounts.spotify.com/api/token"
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # codificar credenciales
    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
    }

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(token_url, data=payload, headers=headers)
    response.raise_for_status()
    #return {"redirect_uri": REDIRECT_URI, "final_url": url}

    return response.json()
    