from fastapi import FastAPI
from database import init_db
from routes import users, chat

app = FastAPI()

# Inicializar la base de datos al iniciar la app
@app.on_event("startup")
def on_startup():
    init_db()

# Incluir los routers
app.include_router(users.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "¡API de chatbot funcionando!"}
