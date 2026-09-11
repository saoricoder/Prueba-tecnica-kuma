from typing import Any, Dict, List
from app.models.schemas import EmpleadoCreate, TareaAssign, TareaCreate
from app.repositories.interfaces import IEmpleadoRepository, ITareaRepository
from fastapi import HTTPException, status

ESTADOS_VALIDOS = {"Pendiente", "En proceso", "Completada"}


class TaskManagementService:
  """Lógica de Negocio (SRP & DIP): Orquesta reglas empresariales."""

  def __init__(
      self, emp_repo: IEmpleadoRepository, tarea_repo: ITareaRepository
  ):
    self.emp_repo = emp_repo
    self.tarea_repo = tarea_repo

  def register_employee(self, data: EmpleadoCreate) -> Dict[str, Any]:
    if self.emp_repo.get_by_email(data.correo):
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"El correo '{data.correo}' ya está registrado.",
      )
    new_id = self.emp_repo.create(data.nombre, data.correo, data.cargo)
    return {"id": new_id, **data.model_dump()}

  def list_employees(self) -> List[Dict[str, Any]]:
    return self.emp_repo.get_all()

  def create_task(self, data: TareaCreate) -> Dict[str, Any]:
    if data.estado not in ESTADOS_VALIDOS:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=(
              "Estado no permitido. Debe ser uno de:"
              f" {', '.join(ESTADOS_VALIDOS)}"
          ),
      )

    if data.empleado_id is not None:
      if not self.emp_repo.get_by_id(data.empleado_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"No existe el empleado con ID {data.empleado_id} para asignar"
                " la tarea."
            ),
        )

    new_id = self.tarea_repo.create(
        data.titulo,
        data.descripcion,
        data.fecha_limite,
        data.estado,
        data.empleado_id,
    )
    return {"id": new_id, **data.model_dump()}

  def list_tasks(self) -> List[Dict[str, Any]]:
    return self.tarea_repo.get_all()

  def assign_task(self, tarea_id: int, payload: TareaAssign) -> Dict[str, Any]:
    if not self.tarea_repo.get_by_id(tarea_id):
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"La tarea #{tarea_id} no existe.",
      )

    empleado = self.emp_repo.get_by_id(payload.empleado_id)
    if not empleado:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"El empleado #{payload.empleado_id} no existe.",
      )

    self.tarea_repo.assign_employee(tarea_id, payload.empleado_id)
    return {
        "mensaje": (
            f"Tarea #{tarea_id} asignada exitosamente a {empleado['nombre']}."
        ),
        "tarea_id": tarea_id,
        "empleado_id": payload.empleado_id,
    }
