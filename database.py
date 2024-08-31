import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Cargar configuraciones de las bases de datos desde el archivo .env
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Conexiones para las bases de datos
DATABASES = {
    'reports_db': {
        'url': f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{os.getenv('DB_HOST1')}:{os.getenv('DB_PORT1')}/{os.getenv('DB_NAME_REPORTS')}",
        'engine': None,
        'session': None
    },
    'accommodation_db': {
        'url': f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{os.getenv('DB_HOST2')}:{os.getenv('DB_PORT2')}/{os.getenv('DB_NAME_ACCOMMODATION')}",
        'engine': None,
        'session': None
    },
    'auth_db': {
        'url': f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{os.getenv('DB_HOST3')}:{os.getenv('DB_PORT3')}/{os.getenv('DB_NAME_AUTH')}",
        'engine': None,
        'session': None
    },
    'events_db': {
        'url': f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{os.getenv('DB_HOST3')}:{os.getenv('DB_PORT3')}/{os.getenv('DB_NAME_EVENTS')}",
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
