"""Punto de entrada principal de la aplicación FastAPI.

Configuración:
- Inicialización de base de datos.
- Middleware CORS.
- Inclusión de rutas API.
- Documentación OpenAPI/Swagger.

Arquitectura:
- Controllers: Enrutamiento y respuestas HTTP.
- Services: Lógica de negocio.
- Repositories: Acceso a datos.
- Database: Gestión de conexiones.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.api_routes import router
from app.database import db_manager

# Inicializar base de datos y crear tablas
db_manager.initialize_tables()

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Tareas",
    description=(
        "API REST para gestión de empleados y asignación de tareas. "
        "Implementa arquitectura MVC con principios SOLID: SRP, OCP, LSP, ISP, DIP. "
        "Utiliza Pydantic para validación tipada, SQLite para persistencia y FastAPI "
        "para exposición de endpoints con documentación automática (OpenAPI/Swagger)."
    ),
    version="1.0.0",
    contact={
        "name": "Prueba Técnica KUMA",
        "url": "https://github.com/saoricoder/Prueba-tecnica-kuma",
    },
)

# Middleware CORS para permitir consumo desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, restringir a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas API
app.include_router(router)


@app.get("/", tags=["Health Check"])
def health_check() -> dict:
    """Verifica que la API está activa y lista.
    
    Returns:
        Dict con estado y mensaje.
    """
    return {
        "status": "ok",
        "message": "Sistema de Gestión de Tareas activo y listo",
        "docs": "http://127.0.0.1:8000/docs",
        "redoc": "http://127.0.0.1:8000/redoc"
    }
