from fastapi import FastAPI
from database import create_reports_tables
from routers import reports
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://front-unlock-patrones.vercel.app",  # Dominio de tu frontend
    "http://localhost:4200",  # Si estás probando en Angular localmente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.on_event("startup")
def on_startup():
    # Crear tablas en la base de datos de reportes al iniciar la aplicación
    create_reports_tables()

app.include_router(reports.router, prefix="/reports", tags=["Reports"])

# Punto de prueba
@app.get("/")
def read_root():
    return {"message": "Welcome to the Reports API"}
