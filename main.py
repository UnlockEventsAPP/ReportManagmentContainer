from fastapi import FastAPI
from database import create_reports_tables
from routers import reports

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # Crear tablas en la base de datos de reportes al iniciar la aplicación
    create_reports_tables()

app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])

# Punto de prueba
@app.get("/")
def read_root():
    return {"message": "Welcome to the Reports API"}
