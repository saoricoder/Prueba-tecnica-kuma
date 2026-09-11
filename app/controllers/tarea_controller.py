"""
Controlador de Tareas - Endpoints REST.

Endpoints:
- POST /tareas: Crear tarea (201 Created)
- GET /tareas: Listar tareas (200 OK)
- PUT /tareas/{id}/asignar: Asignar/reasignar tarea (200 OK)

Códigos HTTP semánticos:
- 201 Created: Recurso creado exitosamente.
- 200 OK: Operación exitosa.
- 400 Bad Request: Datos inválidos.
- 404 Not Found: Tarea o empleado no existe.
- 409 Conflict: Error de integridad.
- 500 Internal Server Error: Error servidor.

SRP: Responsabilidad única de enrutamiento.
DIP: Servicios inyectados mediante FastAPI Depends().
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.models.schemas import TareaCrear, TareaRespuesta, TareaAsignar, TareaConResponsable
from app.services.tarea_service import TareaService
from app.services.empleado_service import EmpleadoService
from app.repositories.tarea_repository import TareaRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.database import db_manager

router = APIRouter(prefix="/tareas", tags=["Tareas"])


def get_tarea_service() -> TareaService:
    """Inyección de dependencia: proporciona el servicio de tareas."""
    tarea_repo = TareaRepository(db_manager)
    empleado_repo = EmpleadoRepository(db_manager)
    return TareaService(tarea_repo, empleado_repo)


def get_empleado_service() -> EmpleadoService:
    """Inyección de dependencia: proporciona el servicio de empleados."""
    repository = EmpleadoRepository(db_manager)
    return EmpleadoService(repository)


@router.post(
    "",
    response_model=TareaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear Tarea",
    description="Crea una nueva tarea con título, fecha límite (ISO YYYY-MM-DD) y asignación opcional.",
    responses={
        201: {"description": "Tarea creada exitosamente"},
        400: {"description": "Datos inválidos"},
        404: {"description": "Empleado no existe"},
        500: {"description": "Error interno del servidor"},
    }
)
def crear_tarea(
    tarea: TareaCrear,
    service: TareaService = Depends(get_tarea_service)
) -> TareaRespuesta:
    """Crea una nueva tarea.
    
    Args:
        tarea: Datos de la tarea (título, descripción, fecha_límite, estado, empleado_id).
        service: Servicio inyectado.
        
    Returns:
        TareaRespuesta con ID asignado.
        
    Raises:
        HTTPException 400: Si los datos son inválidos.
        HTTPException 404: Si el empleado no existe.
    """
    try:
        tarea_creada = service.crear_tarea(
            titulo=tarea.titulo,
            descripcion=tarea.descripcion,
            fecha_limite=tarea.fecha_limite.isoformat(),
            estado=tarea.estado.value,
            empleado_id=tarea.empleado_id
        )
        return TareaRespuesta(**tarea_creada)
    except ValueError as e:
        # Empleado no existe (404)
        if "no existe" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        # Otros errores de validación (400)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear tarea"
        )


@router.get(
    "",
    response_model=List[TareaConResponsable],
    status_code=status.HTTP_200_OK,
    summary="Listar Tareas (con Responsable)",
    description="Obtiene la lista de todas las tareas con información del empleado responsable (JOIN).",
    responses={
        200: {"description": "Lista de tareas con información del responsable"},
        500: {"description": "Error interno del servidor"},
    }
)
def listar_tareas(
    service: TareaService = Depends(get_tarea_service)
) -> List[TareaConResponsable]:
    """Lista todas las tareas con información del responsable.
    
    Args:
        service: Servicio inyectado.
        
    Returns:
        Lista de TareaConResponsable (incluye responsable_nombre y responsable_correo).
    """
    try:
        tareas = service.listar_tareas_con_responsable()
        return [TareaConResponsable(**tarea) for tarea in tareas]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al listar tareas"
        )


@router.put(
    "/{tarea_id}/asignar",
    response_model=TareaRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Asignar/Reasignar Tarea",
    description="Asigna o reasigna una tarea existente a un empleado existente.",
    responses={
        200: {"description": "Tarea asignada exitosamente"},
        400: {"description": "Datos inválidos"},
        404: {"description": "Tarea o empleado no existe"},
        500: {"description": "Error interno del servidor"},
    }
)
def asignar_tarea(
    tarea_id: int,
    asignacion: TareaAsignar,
    service: TareaService = Depends(get_tarea_service)
) -> TareaRespuesta:
    """Asigna o reasigna una tarea a un empleado.
    
    Args:
        tarea_id: ID de la tarea.
        asignacion: Datos con empleado_id.
        service: Servicio inyectado.
        
    Returns:
        TareaRespuesta actualizada.
        
    Raises:
        HTTPException 400: Si los datos son inválidos.
        HTTPException 404: Si la tarea o empleado no existe.
    """
    try:
        tarea_actualizada = service.asignar_tarea(
            tarea_id=tarea_id,
            empleado_id=asignacion.empleado_id
        )
        return TareaRespuesta(**tarea_actualizada)
    except ValueError as e:
        error_msg = str(e).lower()
        # Tarea o empleado no existe (404)
        if "no existe" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        # Otros errores de validación (400)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al asignar tarea"
        )
