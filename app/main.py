from fastapi import FastAPI, UploadFile, File

from app.services.analytics_service import analizar_ventas
from app.utils.file_handler import leer_csv

from sqlalchemy.orm import Session

from app.database.database import (
    SessionLocal,
    engine
)

from app.models.analysis import Analysis
from app.database.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {
        "mensaje": "Smart Sales Analytics API 🚀"
    }

@app.post("/analizar")
async def analizar_csv(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        return {
            "error": "Solo se permiten archivos CSV"
        }

    contenido = await file.read()

    df = leer_csv(contenido)

    resultado = analizar_ventas(df)

    db: Session = SessionLocal()

    nuevo_analisis = Analysis(
        archivo=file.filename,
        ingresos_totales=resultado["ingresos_totales"],
        producto_mas_vendido=resultado["producto_mas_vendido"],
        promedio_venta=resultado["promedio_venta"]
    )

    db.add(nuevo_analisis)

    db.commit()

    db.refresh(nuevo_analisis)

    db.close()

    return {
        "mensaje": "Análisis guardado correctamente",
        "analisis": resultado
    }