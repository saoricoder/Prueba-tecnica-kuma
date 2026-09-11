"""
Pydantic schemas para validación de datos de entrada y respuestas HTTP.

Implementa tipado estricto y validación automática de acuerdo a los requerimientos
del dominio: Empleados (nombre, email único, cargo) y Tareas (título, descripción,
fecha límite ISO YYYY-MM-DD, estados restringidos, relación 1:N con empleados).
"""

from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator


class EstadoTarea(str, Enum):
    """Estados válidos para una tarea (enum restringido)."""
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En proceso"
    COMPLETADA = "Completada"


# ============================================================================
# EMPLEADOS
# ============================================================================

class EmpleadoBase(BaseModel):
    """Modelo base compartido para empleados (entrada)."""
    nombre: str = Field(..., min_length=1, max_length=255, description="Nombre del empleado (requerido)")
    correo: EmailStr = Field(..., description="Correo electrónico válido, único y requerido")
    cargo: str = Field(..., min_length=1, max_length=255, description="Cargo del empleado (requerido)")

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Juan García",
                "correo": "juan.garcia@empresa.com",
                "cargo": "Desarrollador Senior"
            }
        }


class EmpleadoCrear(EmpleadoBase):
    """Schema para crear empleado (POST /empleados)."""
    pass


class EmpleadoRespuesta(EmpleadoBase):
    """Schema de respuesta para empleado (con ID)."""
    id: int = Field(..., description="ID único del empleado (asignado por BD)")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Juan García",
                "correo": "juan.garcia@empresa.com",
                "cargo": "Desarrollador Senior"
            }
        }


# ============================================================================
# TAREAS
# ============================================================================

class TareaBase(BaseModel):
    """Modelo base compartido para tareas (entrada)."""
    titulo: str = Field(..., min_length=1, max_length=255, description="Título de la tarea (requerido)")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Descripción opcional de la tarea")
    fecha_limite: date = Field(..., description="Fecha límite en formato ISO YYYY-MM-DD (requerido)")
    estado: EstadoTarea = Field(EstadoTarea.PENDIENTE, description="Estado: 'Pendiente', 'En proceso', 'Completada' (default: 'Pendiente')")

    @field_validator("fecha_limite", mode="before")
    @classmethod
    def validar_fecha_limite(cls, v):
        """Valida que la fecha sea una fecha válida (puede venir como string ISO o date)."""
        if isinstance(v, str):
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError("Fecha inválida. Formato esperado: YYYY-MM-DD")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Implementar autenticación",
                "descripcion": "Agregar JWT al endpoint /login",
                "fecha_limite": "2024-12-31",
                "estado": "Pendiente"
            }
        }


class TareaCrear(TareaBase):
    """Schema para crear tarea (POST /tareas) - sin empleado_id (asignación opcional inicial)."""
    empleado_id: Optional[int] = Field(None, description="ID del empleado responsable (opcional en creación)")


class TareaAsignar(BaseModel):
    """Schema para asignar/reasignar tarea a empleado (PUT /tareas/{id}/asignar)."""
    empleado_id: int = Field(..., description="ID del empleado al que asignar la tarea")

    class Config:
        json_schema_extra = {
            "example": {
                "empleado_id": 5
            }
        }


class TareaRespuesta(TareaBase):
    """Schema de respuesta para tarea (con ID y datos del responsable)."""
    id: int = Field(..., description="ID único de la tarea (asignado por BD)")
    empleado_id: Optional[int] = Field(None, description="ID del empleado responsable (si aplica)")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "titulo": "Implementar autenticación",
                "descripcion": "Agregar JWT al endpoint /login",
                "fecha_limite": "2024-12-31",
                "estado": "Pendiente",
                "empleado_id": None
            }
        }


class TareaConResponsable(TareaRespuesta):
    """Schema de respuesta con JOIN - incluye datos del empleado responsable."""
    responsable_nombre: Optional[str] = Field(None, description="Nombre del empleado responsable")
    responsable_correo: Optional[str] = Field(None, description="Correo del empleado responsable")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "titulo": "Implementar autenticación",
                "descripcion": "Agregar JWT al endpoint /login",
                "fecha_limite": "2024-12-31",
                "estado": "Pendiente",
                "empleado_id": 5,
                "responsable_nombre": "Juan García",
                "responsable_correo": "juan.garcia@empresa.com"
            }
        }
