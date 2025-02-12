from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import User

router = APIRouter()

@router.get("/health")
def health_check(session: Session = Depends(get_session)):
    try:
        # Verificar si la base de datos está conectada
        session.scalars(select(User).limit(1)).first()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "not connected", "detail": str(e)}
