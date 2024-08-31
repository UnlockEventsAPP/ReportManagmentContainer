from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, db_name
from crud import create_report, get_report
from services.reports_generator import generate_report
from schemas import ReporteCreate, Reporte
router = APIRouter()

@router.post("/generate-report/", response_model=Reporte)
def generate_report_endpoint(
    report: ReporteCreate,
    db: Session = Depends(lambda: next(get_db('reports_db')))
):
    db_report = generate_report(db, report.IdAdministrador)
    return db_report



@router.get("/reportes/{reporte_id}", response_model=Reporte)
def read_report_endpoint(reporte_id: int, db: Session = Depends(lambda: next(get_db('reports_db')))):
    db_report = get_report(db, reporte_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return db_report