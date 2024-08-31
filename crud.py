from sqlalchemy.orm import Session
from models import Reporte
from schemas import ReporteCreate
from datetime import datetime

def create_report(db: Session, report: ReporteCreate) -> Reporte:
    db_reporte = Reporte(**report.dict())
    db.add(db_reporte)
    db.commit()
    db.refresh(db_reporte)
    return db_reporte


def get_report(db: Session, reporte_id: int) -> Reporte:
    return db.query(Reporte).filter(Reporte.IdReporte == reporte_id).first()

def get_reports(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Reporte).offset(skip).limit(limit).all()

def update_report(db: Session, reporte_id: int, updated_reporte: ReporteCreate):
    db_reporte = db.query(Reporte).filter(Reporte.IdReporte == reporte_id).first()
    if db_reporte:
        db_reporte.IdAdministrador = updated_reporte.IdAdministrador
        db_reporte.Contenido = updated_reporte.Contenido
        db.commit()
        db.refresh(db_reporte)
    return db_reporte

def delete_report(db: Session, reporte_id: int):
    db_reporte = db.query(Reporte).filter(Reporte.IdReporte == reporte_id).first()
    if db_reporte:
        db.delete(db_reporte)
        db.commit()
    return db_reporte
