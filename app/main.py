from fastapi import FastAPI, UploadFile, File

from app.services.analytics_service import analizar_ventas
from app.utils.file_handler import leer_csv

app = FastAPI()

@app.get("/")
def home():
    return {
        "mensaje": "Smart Sales Analytics API 🚀"
    }

@app.post("/analizar")
async def analizar_csv(file: UploadFile = File(...)):

    contenido = await file.read()

    df = leer_csv(contenido)

    resultado = analizar_ventas(df)

    return {
        "archivo": file.filename,
        "analisis": resultado
    }