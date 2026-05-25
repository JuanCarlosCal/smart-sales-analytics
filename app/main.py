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
from app.schemas.analysis_schema import AnalysisResponse

Base.metadata.create_all(bind=engine)

from app.services.chart_service import generar_grafico

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/charts", StaticFiles(directory="charts"), name="charts")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home():
    return {
        "mensaje": "Smart Sales Analytics API"
    }

@app.post("/sales/analyze")
async def analizar_csv(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        return {
            "error": "Solo se permiten archivos CSV"
        }

    contenido = await file.read()

    df = leer_csv(contenido)

    resultado = analizar_ventas(df)

    grafico = generar_grafico(df)

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
        "analisis": resultado,
        "grafico": grafico
    }

@app.get("/sales/history", response_model=list[AnalysisResponse])
def obtener_historial():

    db: Session = SessionLocal()

    analyses = db.query(Analysis).all()

    db.close()

    return [
        AnalysisResponse(
            archivo=analysis.archivo,
            ingresos_totales=analysis.ingresos_totales,
            producto_mas_vendido=analysis.producto_mas_vendido,
            promedio_venta=analysis.promedio_venta
        )
        for analysis in analyses
    ]

@app.get("/dashboard")
def dashboard(request: Request):

    db: Session = SessionLocal()

    ultimo = db.query(Analysis).order_by(Analysis.id.desc()).first()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "ingresos": ultimo.ingresos_totales,
            "producto": ultimo.producto_mas_vendido,
            "promedio": ultimo.promedio_venta
        }
    )