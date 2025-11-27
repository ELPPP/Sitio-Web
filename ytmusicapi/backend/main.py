from fastapi import FastAPI
from core_state import HeaderState
from auth import router as auth_router
from Ymusic import router as YmusicClient
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from websocket import start_ws_server  # tu servidor WS externo

# --- Inicialización de la app ---
app = FastAPI()

state = HeaderState.get_instance()

# Routers HTTP normales
app.include_router(auth_router)
app.include_router(YmusicClient)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Backend operativo"}
