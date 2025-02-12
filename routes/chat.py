import openai
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session, engine
from models import User, Message
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Cargar variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está configurada en las variables de entorno")

# Configurar el router
router = APIRouter()

# Definir el esquema para recibir los datos en el body
class ChatRequest(BaseModel):
    username: str
    message: str

# Crear el cliente de OpenAI una sola vez
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@router.post("/ask")
async def ask(request: ChatRequest, session: Session = Depends(get_session)):
    # Verificar si el usuario existe
    user = session.exec(select(User).where(User.username == request.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    try:
        # Llamar a la API de OpenAI con la nueva sintaxis
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": request.message}]
        )

        reply = response.choices[0].message.content

        # Guardar la interacción en la base de datos
        chat_message = Message(username=request.username, question=request.message, response=reply)
        session.add(chat_message)
        session.commit()
        session.refresh(chat_message)

        return {"message": reply}

    except openai.RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Has excedido tu cuota de uso de la API de OpenAI. Por favor, verifica tu plan y facturación."
        )

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")

    finally:
        session.close()

# ✅ Endpoint corregido para consultar el historial de chat por usuario con la URL correcta
@router.get("/history/{username}")
def get_chat_history(username: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    history = session.exec(select(Message).where(Message.username == username).order_by(Message.created_at)).all()
    
    if not history:
        return {"message": "El usuario no tiene historial de conversaciones."}
    
    return {"history": history}

# ✅ Nuevo endpoint para verificar el estado del servicio
@router.get("/health")
def health_check(session: Session = Depends(get_session)):
    try:
        session.exec(select(1))  # Consulta simple para verificar la conexión
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "error", "database": "not connected"}

