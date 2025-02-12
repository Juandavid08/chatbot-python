from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
from models import User, Message  # Importar los modelos
from sqlalchemy.orm import Session

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos desde .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Configurar el motor de SQLite
engine = create_engine(DATABASE_URL, echo=True)

# Función para inicializar la base de datos
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependencia para obtener la sesión de la base de datos
def get_session():
    return Session(engine)  # ✅ Devuelve una sesión sin cerrarla inmediatamente

