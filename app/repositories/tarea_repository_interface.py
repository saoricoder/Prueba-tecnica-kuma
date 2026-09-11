"""
Interfaz abstracta para repositorio de Tareas.

Define el contrato que toda implementación debe cumplir (ISP - Interface Segregation).
Permite desacoplamiento e inyección de dependencias (DIP - Dependency Inversion).
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class ITareaRepository(ABC):
    """Interfaz para operaciones de Tareas (contrato abstracto)."""

    @abstractmethod
    def crear(self, titulo: str, descripcion: Optional[str], fecha_limite: str,
              estado: str = "Pendiente", empleado_id: Optional[int] = None) -> dict:
        """Crea una tarea.
        
        Args:
            titulo: Título de la tarea.
            descripcion: Descripción opcional.
            fecha_limite: Fecha límite en formato ISO YYYY-MM-DD.
            estado: Estado de la tarea (default: 'Pendiente').
            empleado_id: ID del empleado responsable (opcional).
            
        Returns:
            Diccionario con datos de la tarea creada.
            
        Raises:
            ValueError: Si empleado_id no existe o estado inválido.
        """
        pass

    @abstractmethod
    def obtener_por_id(self, tarea_id: int) -> Optional[dict]:
        """Obtiene una tarea por ID.
        
        Args:
            tarea_id: ID de la tarea.
            
        Returns:
            Diccionario con datos de la tarea o None si no existe.
        """
        pass

    @abstractmethod
    def listar_todas(self) -> List[dict]:
        """Lista todas las tareas.
        
        Returns:
            Lista de diccionarios con datos de tareas.
        """
        pass

    @abstractmethod
    def listar_con_responsable(self) -> List[dict]:
        """Lista todas las tareas con JOIN a empleados (incluye nombre y correo del responsable).
        
        Returns:
            Lista de diccionarios con datos de tareas + responsable_nombre y responsable_correo.
        """
        pass

    @abstractmethod
    def asignar(self, tarea_id: int, empleado_id: int) -> dict:
        """Asigna o reasigna una tarea a un empleado.
        
        Args:
            tarea_id: ID de la tarea.
            empleado_id: ID del empleado responsable.
            
        Returns:
            Diccionario con datos de la tarea actualizada.
            
        Raises:
            ValueError: Si la tarea o empleado no existen.
        """
        pass

    @abstractmethod
    def existe(self, tarea_id: int) -> bool:
        """Verifica si existe una tarea con el ID especificado.
        
        Args:
            tarea_id: ID de la tarea.
            
        Returns:
            True si existe, False en caso contrario.
        """
        pass
