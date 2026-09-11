from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IEmpleadoRepository(ABC):

  @abstractmethod
  def create(self, nombre: str, correo: str, cargo: str) -> int:
    pass

  @abstractmethod
  def get_all(self) -> List[Dict[str, Any]]:
    pass

  @abstractmethod
  def get_by_id(self, empleado_id: int) -> Optional[Dict[str, Any]]:
    pass

  @abstractmethod
  def get_by_email(self, correo: str) -> Optional[Dict[str, Any]]:
    pass


class ITareaRepository(ABC):

  @abstractmethod
  def create(
      self,
      titulo: str,
      descripcion: Optional[str],
      fecha_limite: str,
      estado: str,
      empleado_id: Optional[int],
  ) -> int:
    pass

  @abstractmethod
  def get_all(self) -> List[Dict[str, Any]]:
    pass

  @abstractmethod
  def get_by_id(self, tarea_id: int) -> Optional[Dict[str, Any]]:
    pass

  @abstractmethod
  def assign_employee(self, tarea_id: int, empleado_id: int) -> bool:
    pass
