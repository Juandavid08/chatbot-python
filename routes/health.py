from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import User  # Para probar si podemos hacer una consulta

router = APIRouter()

@router.get("/health")
def health_check(session: Session = Depends(get_session)):
    try:
        # Intentar hacer una consulta simple para verificar conexión
        session.exec(select(User).limit(1)).first()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "not connected", "detail": str(e)}
