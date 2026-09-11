"""
Controlador de Empleados - Endpoints REST.

Endpoints:
- POST /empleados: Registrar empleado (201 Created)
- GET /empleados: Listar empleados (200 OK)

Códigos HTTP semánticos:
- 201 Created: Recurso creado exitosamente.
- 200 OK: Operación exitosa.
- 400 Bad Request: Datos inválidos.
- 409 Conflict: Correo duplicado.
- 500 Internal Server Error: Error servidor.

SRP: Responsabilidad única de enrutamiento.
DIP: Servicios inyectados mediante FastAPI Depends().
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.models.schemas import EmpleadoCrear, EmpleadoRespuesta
from app.services.empleado_service import EmpleadoService
from app.repositories.empleado_repository import EmpleadoRepository
from app.database import db_manager

router = APIRouter(prefix="/empleados", tags=["Empleados"])


def get_empleado_service() -> EmpleadoService:
    """Inyección de dependencia: proporciona el servicio de empleados."""
    repository = EmpleadoRepository(db_manager)
    return EmpleadoService(repository)


@router.post(
    "",
    response_model=EmpleadoRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar Empleado",
    description="Crea un nuevo empleado con nombre, correo único y cargo.",
    responses={
        201: {"description": "Empleado creado exitosamente"},
        400: {"description": "Datos inválidos o correo duplicado"},
        500: {"description": "Error interno del servidor"},
    }
)
def crear_empleado(
    empleado: EmpleadoCrear,
    service: EmpleadoService = Depends(get_empleado_service)
) -> EmpleadoRespuesta:
    """Registra un nuevo empleado.
    
    Args:
        empleado: Datos del empleado (nombre, correo, cargo).
        service: Servicio inyectado.
        
    Returns:
        EmpleadoRespuesta con ID asignado.
        
    Raises:
        HTTPException 400: Si los datos son inválidos.
        HTTPException 409: Si el correo ya existe.
    """
    try:
        empleado_creado = service.registrar_empleado(
            nombre=empleado.nombre,
            correo=empleado.correo,
            cargo=empleado.cargo
        )
        return EmpleadoRespuesta(**empleado_creado)
    except ValueError as e:
        # Diferenciar entre correo duplicado (409) y otros errores de validación (400)
        if "ya está registrado" in str(e) or "ya existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear empleado"
        )


@router.get(
    "",
    response_model=List[EmpleadoRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Listar Empleados",
    description="Obtiene la lista de todos los empleados registrados.",
    responses={
        200: {"description": "Lista de empleados"},
        500: {"description": "Error interno del servidor"},
    }
)
def listar_empleados(
    service: EmpleadoService = Depends(get_empleado_service)
) -> List[EmpleadoRespuesta]:
    """Lista todos los empleados registrados.
    
    Args:
        service: Servicio inyectado.
        
    Returns:
        Lista de EmpleadoRespuesta.
    """
    try:
        empleados = service.listar_empleados()
        return [EmpleadoRespuesta(**emp) for emp in empleados]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al listar empleados"
        )
