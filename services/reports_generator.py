import pandas as pd
from sqlalchemy.orm import Session
from database import get_db
from models import Reporte
from schemas import ReporteCreate
from crud import create_report
from io import BytesIO
from sqlalchemy import text
from pathlib import Path

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
    excel_file = generate_in_temporal_memory(accommodation_data, auth_data, events_data)

    return db_reporte


def get_accommodation_data() -> str:
    db = next(get_db('accommodation_db'))
    query = text("SELECT nombre, direccion, precio, status, imagen_url FROM alojamientos")
    results = db.execute(query).fetchall()
    db.close()

    print("Accommodation Data Fetched from DB:", results)  # Depuración
    return "\n".join([f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}" for row in results])


def get_auth_data() -> str:
    db = next(get_db('auth_db'))
    query = text("SELECT nombre, email FROM usuarios")
    results = db.execute(query).fetchall()
    db.close()
    return "\n".join([f"{row[0]} - {row[1]}" for row in results])


def get_events_data() -> str:
    db = next(get_db('events_db'))
    query = text("SELECT nombre, fecha_hora, precio, status FROM eventos")
    results = db.execute(query).fetchall()
    db.close()

    # Asegurarse de que los valores sean cadenas y no nulos
    return "\n".join([
        f"{str(row[0])} - {str(row[1])} - {str(row[2])} - {str(row[3])}" for row in results
    ])

def generate_in_temporal_memory(accommodation_data: str, auth_data: str, events_data: str) -> BytesIO:
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    def create_dataframe(data: str, columns: list) -> pd.DataFrame:
        # Divide las filas basadas en " - " y mapea las columnas correctamente
        rows = [x.split(" - ") for x in data.split("\n") if " - " in x]
        if not rows:  # Si no hay datos, crear un DataFrame vacío
            return pd.DataFrame(columns=columns)
        return pd.DataFrame(rows, columns=columns)

    df_accommodation = create_dataframe(accommodation_data, ["Name", "Location", "Price", "Status", "Image URL"])
    df_auth = create_dataframe(auth_data, ["Username", "Email"])
    print("Events Data:", events_data)
    df_events = create_dataframe(events_data, ["Event Name", "Date", "Price", "Status"])

    df_accommodation.to_excel(writer, sheet_name='Accommodation', index=False)
    df_auth.to_excel(writer, sheet_name='Auth', index=False)
    df_events.to_excel(writer, sheet_name='Events', index=False)

    writer.close()
    output.seek(0)
    return output

def generate_excel(accommodation_data: str, auth_data: str, events_data: str) -> str:
    # Crear un archivo Excel con Pandas
    output_dir = Path("reports")  # Directorio donde se guardará el archivo
    output_dir.mkdir(exist_ok=True)  # Crea el directorio si no existe
    file_path = output_dir / "report.xlsx"  # Ruta completa del archivo

    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    # Convertir los datos a DataFrame
    df_accommodation = pd.DataFrame(
        [x.split(" - ") for x in accommodation_data.split("\n")],
        columns=["Name", "Location", "Price", "Status", "Image URL"]
    )
    df_auth = pd.DataFrame([x.split(" - ") for x in auth_data.split("\n")], columns=["Username", "Email"])
    df_events = pd.DataFrame(
        [x.split(" - ") for x in events_data.split("\n")],
        columns=["Event Name", "Date", "Price", "Status"]
    )

    # Escribir cada DataFrame en una hoja del Excel
    df_accommodation.to_excel(writer, sheet_name='Accommodation', index=False)
    df_auth.to_excel(writer, sheet_name='Auth', index=False)
    df_events.to_excel(writer, sheet_name='Events', index=False)

    # Guardar el archivo Excel
    writer.close()

    return str(file_path)  # Retorna la ruta del archivo guardado

def generate_specific_report(data_function: callable) -> BytesIO:

    data = data_function()
    excel_file = generate_in_temporal_memory(data, "", "")  # Solo utiliza el conjunto de datos específico
    return excel_file
