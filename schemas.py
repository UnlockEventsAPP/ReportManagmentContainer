from pydantic import BaseModel
from datetime import datetime


class ReporteBase(BaseModel):
    Contenido: str = ""
    IdAdministrador: int
    FechaGeneracion: datetime = datetime.now()

class ReporteCreate(ReporteBase):
    pass

class Reporte(ReporteBase):
    IdReporte: int

    class Config:
        from_attributes = True
