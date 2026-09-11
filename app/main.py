from app.controllers.api_routes import router
from app.database import db_manager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Inicializar BD
db_manager.initialize_tables()

app = FastAPI(
    title="Sistema de Gestión de Tareas (MVC + SOLID)",
    description=(
        "Solución con arquitectura por capas, principios SOLID y base de datos"
        " relacional SQLite."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["Health"])
def health_check():
  return {"status": "ok", "message": "API activa y lista"}
