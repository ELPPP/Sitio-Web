from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import auth


app = FastAPI()




#inclusion del archivo auth.py
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "API online"}


# --- DEUDA_TECNICA---
# Ajuste pendiente en el flujo de autenticación de Spotify.
# Estado: flujo operativo, pero incompleto en la persistencia de tokens.
# Descripción:
#   Actualmente se obtiene correctamente el access_token de sesión, 
#   pero no se recupera ni almacena el refresh_token necesario para renovarlo automáticamente.
# Riesgo:
#   Expiración del token de sesión y pérdida temporal de acceso a la API.
# Plan de acción:
#   1. Modificar la función de autenticación para capturar también el refresh_token.
#   2. Implementar almacenamiento seguro (local cifrado o variable de entorno protegida).
#   3. Ajustar el flujo de validación para renovar tokens sin intervención manual.
# Prioridad: Normal (el ajuste es por fines de seguridad, y continuidad y para aumentar la comodidad del cliente)
# --- FIN_DEUDA ---

# --- DEUDA_TECNICA---
# AL FINALIZAR TODO DEBEN CAMBIARSE LOS CLIENT SECRET DEL DASHBOARD, PUES FUERON OTORGADOS A LA IA Y ESO PUEDE SIGNIFICAR UN ERROR DE ALEATORIEDAD
# POR ENDE AL TEMINAR ESTE COMPONENTE DEBEN CAMBIARSE TODAS LAS CREDENCIALES DE PROYECTO
# --- FIN_DEUDA ---



