from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Reporte(Base):
    __tablename__ = "REPORTE"

    IdReporte = Column(Integer, primary_key=True, index=True)
    IdAdministrador = Column(Integer)  # No tiene ForeignKey
    Contenido = Column(String(10000), nullable=False)
    FechaGeneracion = Column(DateTime)