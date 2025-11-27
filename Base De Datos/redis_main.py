# main.py
from fastapi import FastAPI
from worker_routes import router as worker_router

app = FastAPI(title="MusicSync API")

app.include_router(worker_router, prefix="/worker")

# Variables globales simulando la BD volátil
playlists = {}
playlists_backup = {}
playlists_ordered = {}
relations = {}
db_status = "uninitialized"

@app.on_event("startup")
def startup_event():
    global playlists, playlists_backup, playlists_ordered, relations, db_status

    playlists = {}
    playlists_backup = {}
    playlists_ordered = {}
    relations = {}
    relations_index={}
    db_status = "initialized"
    Nrel:0

    print("[INIT] Base de datos temporal inicializada correctamente.")


# ==========================
# Ruta de diagnóstico
# ==========================
@app.get("/status")
def status():
    return {"db_status": db_status, "playlists": len(playlists), "relations": len(relations)}

