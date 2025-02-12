from fastapi import APIRouter, Depends, HTTPException # Importar HTTPException
from sqlmodel import Session, select
from database import get_session
from models import User #   Importar el modelo User
from pydantic import BaseModel

# Creamos un router
router = APIRouter()

# Definir un esquema Pydantic para la solicitud
class UserCreate(BaseModel):
    username: str
    role: str

@router.post("/init_user")
def init_user(user: UserCreate, session: Session = Depends(get_session)):
    # Verificar si el usuario ya existe
    existing_user = session.scalars(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Creamos un nuevo usuario
    new_user = User(username=user.username, role=user.role)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Retornamos un mensaje y el usuario creado
    return {"message": "Usuario creado", "user": new_user}
