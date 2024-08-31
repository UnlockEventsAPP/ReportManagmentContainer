import pandas as pd
from sqlalchemy.orm import Session
from database import get_db
from models import Reporte
from schemas import ReporteCreate
from crud import create_report
from io import BytesIO
from sqlalchemy import text

def generate_report(db: Session, admin_id: int) -> Reporte:
    # Obtener la información de las diferentes bases de datos
    accommodation_data = get_accommodation_data()
    auth_data = get_auth_data()
    events_data = get_events_data()

    # Combinar la información en un string para guardar en la base de datos
    report_content = f"Accommodation Data:\n{accommodation_data}\n\n"
    report_content += f"Auth Data:\n{auth_data}\n\n"
    report_content += f"Events Data:\n{events_data}\n\n"

    # Crear un nuevo reporte en la base de datos
    new_report = ReporteCreate(
        IdAdministrador=admin_id,
        Contenido=report_content
    )

    # Guardar el reporte en la base de datos
    db = next(get_db('reports_db'))  # Consumir el generador aquí
    db_reporte = create_report(db, new_report)

    # Generar un archivo Excel con la información
    excel_file = generate_excel(accommodation_data, auth_data, events_data)

    return db_reporte



def get_accommodation_data() -> str:
    db = next(get_db('accommodation_db'))
    # Realiza la consulta para obtener los datos de la base de datos de alojamiento
    query = text("SELECT nombre, direccion FROM alojamientos")
    results = db.execute(query).fetchall()
    db.close()  # Asegurarse de cerrar la conexión
    return "\n".join([f"{row[0]} - {row[1]}" for row in results])

def get_auth_data() -> str:
    db = next(get_db('auth_db'))
    # Realiza la consulta para obtener los datos de la base de datos de autenticación
    query = text("SELECT nombre, email FROM usuarios")
    results = db.execute(query).fetchall()
    db.close()  # Asegurarse de cerrar la conexión
    return "\n".join([f"{row[0]} - {row[1]}" for row in results])

def get_events_data() -> str:
    db = next(get_db('events_db'))
    # Realiza la consulta para obtener los datos de la base de datos de eventos
    query = text("SELECT nombre, fecha_hora FROM eventos")
    results = db.execute(query).fetchall()
    db.close()  # Asegurarse de cerrar la conexión
    return "\n".join([f"{row[0]} - {row[1]}" for row in results])


def generate_excel(accommodation_data: str, auth_data: str, events_data: str) -> BytesIO:
    # Crear un archivo Excel con Pandas
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # Convertir los datos a DataFrame
    df_accommodation = pd.DataFrame([x.split(" - ") for x in accommodation_data.split("\n")],
                                    columns=["Name", "Location"])
    df_auth = pd.DataFrame([x.split(" - ") for x in auth_data.split("\n")], columns=["Username", "Email"])
    df_events = pd.DataFrame([x.split(" - ") for x in events_data.split("\n")], columns=["Event Name", "Date"])

    # Escribir cada DataFrame en una hoja del Excel
    df_accommodation.to_excel(writer, sheet_name='Accommodation', index=False)
    df_auth.to_excel(writer, sheet_name='Auth', index=False)
    df_events.to_excel(writer, sheet_name='Events', index=False)

    # Cerrar el archivo Excel para guardar el contenido
    writer.close()
    output.seek(0)  # Volver al inicio del archivo para la lectura posterior
    return output

