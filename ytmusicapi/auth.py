from core_state import HeaderState
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket, WebSocketDisconnect
from uuid import uuid4
import secrets
import time
import asyncio
import random
import asyncio
from typing import Union

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class DisableOriginCheckMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Para WebSockets, esto NO se ejecuta, pero fuerza el ASGI a no aplicar su filtro
        request.headers.__dict__["_list"] = [
            (b"origin", b"*")
        ] + request.headers.raw
        return await call_next(request)

app.add_middleware(DisableOriginCheckMiddleware)


  # importa el singleton desde main o core.state





active_connection: Union[WebSocket, None] = None
active_token: Union[str, None] = None
CONNECTION_TIMEOUT = 60



def get_auth_router(state):
    router = APIRouter()

    @router.websocket("/auth/ytm/ws")
    async def websocket_auth_ytm(ws: WebSocket):
        global active_connection, active_token
    
        # --- ORIGEN ---
        origin = ws.headers.get("origin", "")
        print("origin:", origin)
    
        allowed_prefix = "chrome-extension://koljknhbmamjmhhgeddfdamlmlaonamo"
        allowed_origins = {
            "http://127.0.0.1:8002",
            "http://localhost:8002",
        }
    
        origin_ok = (
            origin.startswith(allowed_prefix) or
            origin in allowed_origins
        )
    
        # Si YA hay conexión activa → rechazamos
        if active_connection is not None:
            await ws.accept()
            await ws.send_json({"error": "conexion_activa"})
            await ws.close()
            return
    
        # Si el origin NO es válido → rechazamos
        if not origin_ok:
            await ws.accept()
            await ws.send_json({"error": "origin_no_permitido"})
            await ws.close()
            return
    
        # --- Aceptamos SOLO UNA VEZ ---
        await ws.accept()
    
        # Guardamos conexión
        active_connection = ws
        active_token = uuid4().hex
    
        print("[WS] Nueva conexión aceptada.")
        await ws.send_json({"token": active_token, "nonce": state.New_nonce})
    
        try:
            while True:
                try:
                    data = await asyncio.wait_for(ws.receive_json(), timeout=CONNECTION_TIMEOUT)
                except asyncio.TimeoutError:
                    print("[WS] Timeout: cerrando conexión por inactividad.")
                    break
                
                received_token = data.get("token")
    
                if received_token != active_token:
                    await ws.send_json({"error": "token_invalido"})
                    continue
                
                # nuevo token
                active_token = uuid4().hex
    
                nonce_value = getattr(state, "New_nonce", None)
    
                await ws.send_json({"token": active_token, "nonce": nonce_value})
    
        except WebSocketDisconnect:
            print("[WS] Conexión cerrada por el cliente.")
        except Exception as e:
            print(f"[WS] Error inesperado: {e}")
        finally:
            active_connection = None
            active_token = None
            await ws.close()
            print("[WS] Conexión liberada y cerrada.")




    @router.post("/auth/ytm/request")
    async def request_nonce(request: Request):
        """
        Endpoint que coordina el flujo inicial de autorización:
        - Genera un nuevo nonce.
        - Cambia el estado a "waiting".
        - Notifica a la extensión que debe enviar headers.
        """

        

        # --- BLOQUE 1: Lectura y diagnóstico del estado actual ---
        current_status = getattr(state, "status", "unknown")
        current_nonce = getattr(state, "_nonce", None)
        last_update = getattr(state, "_timestamp", None)

        print(f"[AUTH-A] Estado actual -> {current_status}, nonce={current_nonce}, ts={last_update}")

        # --- BLOQUE 2: Si el estado actual está "ok" o "ready", se inicia nuevo ciclo ---
        # (asumimos que los headers actuales son válidos y el usuario pide revalidación)
        if current_status in ("ok", "ready", None, "init"):
            new_nonce = secrets.token_hex(8)  # nonce aleatorio corto
            state.New_nonce = new_nonce# --- Envío del nonce al singleton
            print("nonce enviado al singleton")
            state._timestamp = time.time()
            state.status = "waiting"
            print(f"[AUTH-A] Nuevo ciclo iniciado, nonce={new_nonce}")
            print("señor usuario, autorize la lectura de headers en la extension, gracias :)")

            return JSONResponse({
                "status": "waiting",
                "nonce": new_nonce,
                "message": "Nuevo nonce generado, esperando headers desde la extensión."
            })

        # --- BLOQUE 3: Si ya hay un proceso pendiente, no se genera otro nonce ---
        elif current_status == "waiting":
            print("[AUTH-A] Petición recibida mientras se espera headers.")
            return JSONResponse({
                "status": "waiting",
                "nonce": current_nonce,
                "message": "Ya existe un proceso de validación en curso."
            })

        # --- BLOQUE 4: Estado inesperado (fallback defensivo) ---

        else:
            # --- HONEYPOT: respuesta aleatoria, logging y backoff no bloqueante ---
            messages = [
                "Felicidades: descubriste el hueco donde las leyes de la lógica van a perderse. No hay nonce para ti.",
                "Nice try. Has inventado un tercer estado. Aquí no repartimos chocolatinas a experimentos.",
                "Error: has puesto quinta pata al gato. Estado inválido — operación abortada.",
                "Enhorabuena, desbloqueaste el modo 'no espera/no servicio'. No vamos a jugar.",
                "Estado inválido detectado. Esto no es un juego, vuelve cuando seas humano."
            ]

            chosen = random.choice(messages)

            # Log en servidor (útil para auditoría)
            tries = getattr(state, "_honeypot_hits", 0) + 1
            state._honeypot_hits = tries
            print(f"[AUTH-A][HONEYPOT] estado_invalido='{current_status}', reply='{chosen}', hits={tries}")

            # backoff no bloqueante (0.25s * hits, cap 2s)
            backoff = min(2.0, 0.25 * tries)
            print(f"[AUTH-A][HONEYPOT] aplicando backoff no bloqueante de {backoff:.2f}s")
            await asyncio.sleep(backoff)

            # Respuesta al cliente (con actitud pero sin revelar detalles sensibles)
            return JSONResponse({
                "status": "error",
                "message": chosen,
                "honeypot_hits": tries
            }, status_code=400)





    @router.post("/auth/ytm/headers")
    async def receive_headers(request: Request):
        """
        Endpoint B: recibe los headers desde la extensión del navegador,
        valida el nonce y actualiza los datos en memoria global.
        """
        # --- BLOQUE 1: Parseo y validación básica del JSON recibido ---
        try:
            data = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="invalid json")

        cookie = data.get("cookie")
        user_agent = data.get("user_agent")
        nonce = data.get("nonce")  # nonce devuelto por la extensión

        if not cookie or not nonce:
            raise HTTPException(status_code=400, detail="missing cookie or nonce")

        # --- BLOQUE 2: Validar nonce actual ---
        current_nonce = getattr(state, "New_nonce", None)

        if current_nonce is None:
            # no hay nonce activo; significa que nadie pidió headers
            raise HTTPException(status_code=400, detail="no active nonce; nothing to update")

        if nonce != current_nonce:
            # nonce incorrecto → posible duplicado, intento viejo o error de sincronización
            print(f"[AUTH-B] Nonce inválido recibido: {nonce} (esperado {current_nonce})")
            state.status = "ok"  # desbloquea flujo para reintento posterior
            return JSONResponse({
                "ok": False,
                "status": "nonce_mismatch",
                "message": "Nonce incorrecto o expirado, ignorando datos."
            })

        # --- BLOQUE 3: Actualizar headers en el singleton ---
        now = time.time()
        entry = {
            "received_at": now,
            "cookie_trunc": cookie[:200],
            "full": cookie,
            "user_agent": user_agent,
            "origin": data.get("origin"),
            "referer": data.get("referer"),
            "nonce": nonce,
        }

        # guardamos en memoria global
        state.headers = entry
        state.status = "ok"  # listo para usarse
        state._timestamp = now
        state.New_nonce = None

        print("=== [AUTH-B] Headers actualizados correctamente ===")
        print(f"Nonce: {nonce}")
        print(f"User-Agent: {user_agent}")
        print(f"Cookie: {cookie[:100]}...")
        print("===================================================")

        # --- BLOQUE 4: Respuesta final ---
        return JSONResponse({
            "ok": True,
            "status": "ok",
            "message": "Headers recibidos y validados correctamente.",
            "timestamp": now
        })
    return router