"""
Enrutador principal de la API.

Combina todos los controladores (empleados y tareas) en un único router.
Proporciona punto único de entrada para la API.
"""

from fastapi import APIRouter
from app.controllers.empleado_controller import router as empleado_router
from app.controllers.tarea_controller import router as tarea_router

router = APIRouter(prefix="/api/v1")
router.include_router(empleado_router)
router.include_router(tarea_router)
