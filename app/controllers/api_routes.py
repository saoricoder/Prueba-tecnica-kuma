from typing import List
from app.models.schemas import EmpleadoCreate, EmpleadoResponse, TareaAssign, TareaCreate, TareaResponse
from app.repositories.sqlite_repository import SQLiteEmpleadoRepository, SQLiteTareaRepository
from app.services.task_service import TaskManagementService
from fastapi import APIRouter, Depends, status

router = APIRouter()


def get_service() -> TaskManagementService:
  emp_repo = SQLiteEmpleadoRepository()
  tarea_repo = SQLiteTareaRepository()
  return TaskManagementService(emp_repo=emp_repo, tarea_repo=tarea_repo)


@router.post(
    "/empleados",
    response_model=EmpleadoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Empleados"],
)
def registrar_empleado(
    data: EmpleadoCreate, service: TaskManagementService = Depends(get_service)
):
  return service.register_employee(data)


@router.get(
    "/empleados", response_model=List[EmpleadoResponse], tags=["Empleados"]
)
def listar_empleados(service: TaskManagementService = Depends(get_service)):
  return service.list_employees()


@router.post(
    "/tareas",
    response_model=TareaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tareas"],
)
def crear_tarea(
    data: TareaCreate, service: TaskManagementService = Depends(get_service)
):
  return service.create_task(data)


@router.get("/tareas", response_model=List[TareaResponse], tags=["Tareas"])
def listar_tareas(service: TaskManagementService = Depends(get_service)):
  return service.list_tasks()


@router.put("/tareas/{tarea_id}/asignar", tags=["Tareas"])
def asignar_tarea(
    tarea_id: int,
    payload: TareaAssign,
    service: TaskManagementService = Depends(get_service),
):
  return service.assign_task(tarea_id, payload)
