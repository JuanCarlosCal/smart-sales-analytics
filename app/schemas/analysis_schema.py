from pydantic import BaseModel

class AnalysisResponse(BaseModel):

    archivo: str

    ingresos_totales: float

    producto_mas_vendido: str

    promedio_venta: float