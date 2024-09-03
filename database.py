import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Cargar configuraciones de las bases de datos desde el archivo .env
URL = os.getenv("DB_URL")
AURL = os.getenv("ACCOMMODATION_URL")
AUURL = os.getenv("AUTH_DB")
EVURL = os.getenv("EVENTS_DB")
#DB_URL=mysql+pymysql://develop:1234@localhost:3306/reports_db
#ACCOMMODATION_URL=mysql+pymysql://develop:1234@localhost:3306/accommodation_db
#AUTH_DB=mysql+pymysql://develop:1234@localhost:3306/auth_db
#EVENTS_DB=mysql+pymysql://develop:1234@localhost:3306/events_db



# Conexiones para las bases de datos
DATABASES = {
    'reports_db': {
        'url': f"{URL}",
        'engine': None,
        'session': None
    },
    'accommodation_db': {
        'url': f"{AURL}",
        'engine': None,
        'session': None
    },
    'auth_db': {
        'url': f"{AUURL}",
        'engine': None,
        'session': None
    },
    'events_db': {
        'url': f"{EVURL}",
        'engine': None,
        'session': None
    }
}

# Crear engines y sessionmakers para cada base de datos
for db_name, db_info in DATABASES.items():
    engine = create_engine(db_info['url'])
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    DATABASES[db_name]['engine'] = engine
    DATABASES[db_name]['session'] = session

Base = declarative_base()

def get_db(db_name: str):
    """Obtiene la sesión de la base de datos especificada."""
    db_session = DATABASES[db_name]['session']()
    try:
        yield db_session
    finally:
        db_session.close()

def create_reports_tables():
    """Crea las tablas de la base de datos reports_db si no existen."""
    Base.metadata.create_all(bind=DATABASES['reports_db']['engine'])
