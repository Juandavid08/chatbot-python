# chatbot-python
<span style="color:blue"> Desarrollo de chatbot integrando OpenAI</span>


# 🧠 Chatbot-Python

#### Este proyecto es un **chatbot** desarrollado en el framework **FastAPI** que interactúa con la API de **OpenAI** y almacena el historial de conversaciones en una base de datos **SQL**. También incluye endpoints para la gestión de usuarios y verificación del estado del sistema.


---


## 📌 <span style="color:red"> Características </span>

✅ Creacion de usuario con rol
✅ Integracion con **OpenAI GPT** para respuestas automatizadas.  
✅ Almacenamiento de historial de conversaciones.  
✅ API documentada con **Swagger** (autogenerado por FastAPI).  
✅ Validación del estado de la base de datos.  


---


## ⚙️ <span style="color:red">Instalación y configuración </span>

### 1️⃣ **Clonar el repositorio**

git clone https://github.com/Juandavid08/chatbot-python.git

---

### 2️⃣ **Crear un entorno virtual y activarlo**

python -m venv venv
venv\Scripts\activate


---


### 3️⃣ **Instalar dependencias necesarias**

pip install fastapi uvicorn sqlmodel sqlalchemy openai python-dotenv requirements.txt


---


### 4️⃣ **Configurar variables de entorno**
Crea un archivo .env en la raíz del proyecto y agrega:

OPENAI_API_KEY= clave proporcionada por openAI
DATABASE_URL=sqlite:///./database.db

> NOTA: Verificar que la keys tenga total disponibilidad para ser usada


---


### 5️⃣ **Ejecutar la aplicación**
uvicorn main:app --reload


---


## 🚀 **Uso de la API**

### Documentación interactiva
Después de iniciar el servidor, puedes acceder a la documentación generada automáticamente por FastAPI en:

Swagger: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc


### Estructura de la base de datos

#### Tabla message

| id       | username | question  | response | created_at|
|----------|----------|-----------|----------|-----------|
|          |          |           |          |           |
|          |          |           |          |           |

#### Tabla user

| id       | username | role      |
|----------|----------|-----------|
|          |          |           |
|          |          |           |


---


### 🔬 Pruebas unitarias
Ejecuta las pruebas con:
pytest


---


### 🎯 Decisiones técnicas tomada
FastAPI fue elegido por su alto rendimiento y facilidad de uso.
SQLModel se usa para la gestión de la base de datos, combinando lo mejor de SQLAlchemy y Pydantic.
OpenAI API se integra para la generación de respuestas inteligentes.
Swagger se usa para documentar la API automáticamente.


> Emogis sacados de: 

https://emojipedia.org/
https://github.com/ikatyang/emoji-cheat-sheet