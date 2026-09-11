from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# --- DTOs Empleado ---
class EmpleadoBase(BaseModel):
  nombre: str = Field(..., min_length=2, example="Ana Pérez")
  correo: EmailStr = Field(..., example="ana.perez@empresa.com")
  cargo: str = Field(..., min_length=2, example="Desarrolladora Backend")


class EmpleadoCreate(EmpleadoBase):
  pass


class EmpleadoResponse(EmpleadoBase):
  id: int


# --- DTOs Tarea ---
class TareaBase(BaseModel):
  titulo: str = Field(..., min_length=2, example="Diseñar arquitectura de BD")
  descripcion: Optional[str] = Field(
      None, example="Modelado relacional y claves foráneas"
  )
  fecha_limite: str = Field(..., example="2026-10-15")
  estado: str = Field("Pendiente", example="Pendiente")


class TareaCreate(TareaBase):
  empleado_id: Optional[int] = Field(None, example=1)


class TareaAssign(BaseModel):
  empleado_id: int = Field(..., example=1)


class TareaResponse(BaseModel):
  id: int
  titulo: str
  descripcion: Optional[str]
  fecha_limite: str
  estado: str
  empleado_id: Optional[int] = None
  responsable_nombre: Optional[str] = None
  responsable_correo: Optional[str] = None
