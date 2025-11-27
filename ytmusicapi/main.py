from fastapi import FastAPI
from core_state import HeaderState
from auth import get_auth_router
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI, Request
os.environ["WSGI_SERVER"] = "uvicorn"  # no afecta
os.environ["WEBSOCKET_MAX_SIZE"] = "16777216"
os.environ["WEBSOCKET_MAX_QUEUE"] = "32"
os.environ["WEBSOCKET_TIMEOUT"] = "30"
os.environ["WEBSOCKET_PING_INTERVAL"] = "20"

# --- Singleton global de estado ---
app = FastAPI()

@app.middleware("http")
async def debug_origin(request: Request, call_next):
    origin = request.headers.get("origin")
    print(">>> ORIGIN RECIBIDO:", origin)
    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inicialización de la app ---
state = HeaderState.get_instance()
auth_router = get_auth_router(state)
app.include_router(auth_router, prefix="/auth/ytm", tags=["YouTube Music Auth"])

# CORS



@app.get("/")
async def root():
    return {"status": "ok", "message": "Backend operativo"}
