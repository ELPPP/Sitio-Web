from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import auth


app = FastAPI()




#inclusion del archivo auth.py
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "API online"}





