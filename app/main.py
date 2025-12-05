from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from src.features.db.db_config import engine, get_db
from src.features.event.presentation.controller_event import router as event_router


app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "https://jalatealciclismo.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

app.include_router(event_router)

@app.get("/")
def root():
    return {"message": "API corriendo correctamente"}

@app.get("/test")
def test_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()  # obtiene el valor simple (1)
            return {"db_status": "Conectado", "result": value}
    except Exception as e:
        print("Error de conexión:", e)
        return {"db_status": "Error", "details": str(e)}
    