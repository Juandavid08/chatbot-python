from fastapi import FastAPI
from database import init_db
from routes import users, chat, health  # Importar health

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

# Incluir los routers
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(health.router)  # Agregar el router de health

@app.get("/")
def read_root():
    return {"message": "¡API de chatbot funcionando!"}
