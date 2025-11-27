# worker_routes.py
from fastapi import APIRouter, HTTPException, status, Header
from typing import Dict, Any, Optional
from uuid import uuid4
from copy import deepcopy
import redis
import json


router = APIRouter()


# conexión temporal a redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

router = APIRouter()

@router.post("/add_song")
def add_song(arreglo: dict, mode: str, batch: bool = False):
    """
    Agrega una o múltiples canciones al arreglo Redis correspondiente.
    mode: playlists, playlist_backup, playlist_sorted
    arreglo: diccionario con las canciones
    batch: True para mantener conexión abierta, False para cerrar tras la operación
    """

    # obtener data actual
    data_str = r.get(mode)
    if data_str:
        data = json.loads(data_str)
    else:
        data = {}

    # agregar canciones
    for song_id, song_data in arreglo.items():
        prefix = song_id[:2].lower()  # sp, yt, lc
        if prefix not in data:
            data[prefix] = {}
        data[prefix][song_id] = song_data

    # guardar cambios
    r.set(mode, json.dumps(data))

    # cerrar conexión si no es batch
    if not batch:
        r.close()

    return {"status": "ok", "added": list(arreglo.keys()), "mode": mode}


@router.get("/get_song")
def get_song(id, mode: str = "playlists"):
    """
    Obtiene una o varias canciones de las estructuras Redis.
    - id puede ser un string (una sola canción) o una lista (varias).
    - mode define qué conjunto usar: playlists, playlists_backup o playlists_sorted.
    """
    try:
        # Cargar el arreglo correspondiente desde Redis
        data_raw = r.get(mode)
        if not data_raw:
            return {"error": f"No se encontró el arreglo {mode} en Redis"}
        playlists = json.loads(data_raw)

        # Función auxiliar para obtener una canción
        def obtener(id_str):
            prefix = id_str[:2]  # sp, yt, lc
            if prefix not in playlists:
                return {"error": f"Fuente {prefix} no encontrada"}
            return playlists[prefix].get(id_str, {"error": f"ID {id_str} no encontrado"})

        # Si el ID es lista → devolver varias
        if isinstance(id, list):
            return [obtener(i) for i in id]
        # Si el ID es string → devolver una
        elif isinstance(id, str):
            return obtener(id)
        else:
            return {"error": "El parámetro id debe ser string o lista"}

    except Exception as e:
        return {"error": str(e)}





@router.post("/link_relation/")
async def link_relation(id1: str, id2: str):
    """
    Crea o actualiza relaciones entre canciones de distintas plataformas.
    Usa:
      - 'relations' → guarda las relaciones reales.
      - 'relation_index' → mapea IDs individuales a su relación.
      - 'Nrel' → contador global de relaciones.
    """

    # ---- Verificar existencia de Nrel ----
    Nrel = await redis.get("Nrel")
    if Nrel is None:
        raise HTTPException(status_code=500, detail="Variable 'Nrel' no inicializada en Redis.")
    Nrel = int(Nrel)

    # ---- Cargar estructuras ----
    relation_index_raw = await redis.get("relation_index")
    relations_raw = await redis.get("relations")

    relation_index = json.loads(relation_index_raw) if relation_index_raw else {}
    relations = json.loads(relations_raw) if relations_raw else {}

    rel1 = relation_index.get(id1)
    rel2 = relation_index.get(id2)

    # ---- Caso 1: ambos IDs ya están en relaciones distintas ----
    if rel1 and rel2 and rel1 != rel2:
        # Aquí se podría hacer trazabilidad o fusión, pero por ahora seguridad
        await call_security_method(rel1, rel2)
        return {"status": "alert", "message": f"Conflicto detectado entre {rel1} y {rel2}. Seguridad invocada."}

    # ---- Caso 2: ambos IDs ya están en la misma relación ----
    if rel1 == rel2 and rel1 is not None:
        return {"status": "ok", "message": f"IDs {id1} y {id2} ya pertenecen a la relación {rel1}."}

    # ---- Caso 3: uno de los dos tiene relación, se agrega el otro ----
    if rel1 or rel2:
        current_rel = rel1 or rel2
        relations[current_rel].append(id1 if not rel1 else id2)
        relation_index[id1 if not rel1 else id2] = current_rel

        # Comprobación de umbral (si pasa de 6 elementos)
        if len(relations[current_rel]) > 6:
            await call_security_method(current_rel)
            return {"status": "warning", "message": f"Relación {current_rel} excede límite (7 IDs). Seguridad invocada."}

        # Guardar cambios
        await redis.set("relations", json.dumps(relations))
        await redis.set("relation_index", json.dumps(relation_index))

        return {"status": "updated", "message": f"Se añadió {id1 if not rel1 else id2} a {current_rel}."}

    # ---- Caso 4: ninguno de los dos tiene relación → crear nueva ----
    new_relation_id = f"IDR{Nrel + 1}"

    relations[new_relation_id] = [id1, id2]
    relation_index[id1] = new_relation_id
    relation_index[id2] = new_relation_id

    # Actualizar contador Nrel
    await redis.set("Nrel", Nrel + 1)

    # Guardar cambios
    await redis.set("relations", json.dumps(relations))
    await redis.set("relation_index", json.dumps(relation_index))

    return {"status": "created", "message": f"Creada nueva relación {new_relation_id} con {id1} y {id2}."}


# ---- Método de seguridad (placeholder) ----
async def call_security_method(*args):
    """
    Placeholder para el sistema de seguridad.
    Se activará si se detecta una condición peligrosa o incoherente.
    """
    print(f"[SECURITY] Activado con parámetros: {args}")
    # Aquí se montará la lógica IA o correctiva en el futuro
