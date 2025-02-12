from sqlmodel import SQLModel, Field
from typing import Optional # Importamos el tipo de dato Optional
from datetime import datetime # Importamos el tipo de dato datetime


# Modelo para la tabla de usuarios
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    role: str

# Modelo para la tabla de mensajes
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    question: str
    response: str
    created_at: datetime = Field(default_factory=datetime.now)  

