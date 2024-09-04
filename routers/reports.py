from fastapi import APIRouter, Depends, HTTPException, Response, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db, db_name
from crud import create_report, get_report
from services.reports_generator import generate_report, generate_in_temporal_memory, get_events_data, get_auth_data, \
    get_accommodation_data, generate_excel, generate_specific_report
from schemas import ReporteCreate, Reporte
from services.rabbit_connection import send_to_rabbitmq
router = APIRouter()


@router.post("/generate-report/", response_model=Reporte)
def generate_report_endpoint(
        report: ReporteCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(lambda: next(get_db('reports_db')))
):
    db_report = generate_report(db, report.IdAdministrador)

    report_data = {
        "report_id": db_report.IdReporte,
        "admin_id": report.IdAdministrador,
        "report_type": "general",
        "content": db_report.Contenido
    }

    # Enviar a RabbitMQ en segundo plano
    background_tasks.add_task(send_to_rabbitmq, report_data)

    return db_report



@router.get("/reportes/{reporte_id}", response_model=Reporte)
def read_report_endpoint(reporte_id: int, db: Session = Depends(lambda: next(get_db('reports_db')))):
    db_report = get_report(db, reporte_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return db_report

# Endpoint para generar y devolver el reporte en memoria
@router.get("/download-report/accommodation/", response_class=Response)
def download_accommodation_report(db: Session = Depends(lambda: get_db('reports_db'))):
    excel_file = generate_specific_report(get_accommodation_data)
    headers = {'Content-Disposition': 'attachment; filename="accommodation_report.xlsx"'}
    return Response(content=excel_file.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

@router.get("/download-report/auth/", response_class=Response)
def download_auth_report(db: Session = Depends(lambda: get_db('reports_db'))):
    excel_file = generate_specific_report(get_auth_data)
    headers = {'Content-Disposition': 'attachment; filename="auth_report.xlsx"'}
    return Response(content=excel_file.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

@router.get("/download-report/events/", response_class=Response)
def download_events_report(db: Session = Depends(lambda: get_db('reports_db'))):
    excel_file = generate_specific_report(get_events_data)
    headers = {'Content-Disposition': 'attachment; filename="events_report.xlsx"'}
    return Response(content=excel_file.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)