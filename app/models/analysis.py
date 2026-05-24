from sqlalchemy import Column, Integer, Float, String

from app.database.database import Base

class Analysis(Base):

    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)

    archivo = Column(String)

    ingresos_totales = Column(Float)

    producto_mas_vendido = Column(String)

    promedio_venta = Column(Float)