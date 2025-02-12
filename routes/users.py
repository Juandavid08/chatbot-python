from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import User
from pydantic import BaseModel

router = APIRouter()

# Definir un esquema Pydantic para la solicitud
class UserCreate(BaseModel):
    username: str
    role: str

@router.post("/init_user")
def init_user(user: UserCreate, session: Session = Depends(get_session)):
    # Verificar si el usuario ya existe
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    new_user = User(username=user.username, role=user.role)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "Usuario creado", "user": new_user}
