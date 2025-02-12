import openai
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
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

# Definir los esquemas
class ChatRequest(BaseModel):
    username: str
    message: str

# Crear el cliente de OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@router.post("/ask")
async def ask(request: ChatRequest, session: Session = Depends(get_session)):
    user = session.scalars(select(User).where(User.username == request.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": request.message}]
        )
        reply = response.choices[0].message.content

        chat_message = Message(username=request.username, question=request.message, response=reply)
        session.add(chat_message)
        session.commit()
        session.refresh(chat_message)

        return {"message": reply}

    except openai.RateLimitError:
        raise HTTPException(status_code=429, detail="Límite de uso de OpenAI excedido.")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")
    finally:
        session.close()

@router.get("/history/{username}")
def get_chat_history(username: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    history = session.exec(select(Message).where(Message.username == username).order_by(Message.created_at)).all()
    return {"history": history if history else "El usuario no tiene historial de conversaciones."}
