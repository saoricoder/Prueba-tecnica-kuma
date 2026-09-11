"""
Interfaz abstracta para repositorio de Empleados.

Define el contrato que toda implementación debe cumplir (ISP - Interface Segregation).
Permite desacoplamiento e inyección de dependencias (DIP - Dependency Inversion).
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class IEmpleadoRepository(ABC):
    """Interfaz para operaciones de Empleados (contrato abstracto)."""

    @abstractmethod
    def crear(self, nombre: str, correo: str, cargo: str) -> dict:
        """Crea un empleado.
        
        Args:
            nombre: Nombre del empleado.
            correo: Correo electrónico único.
            cargo: Cargo del empleado.
            
        Returns:
            Diccionario con datos del empleado creado (id, nombre, correo, cargo).
            
        Raises:
            ValueError: Si el correo ya existe.
        """
        pass

    @abstractmethod
    def obtener_por_id(self, empleado_id: int) -> Optional[dict]:
        """Obtiene un empleado por ID.
        
        Args:
            empleado_id: ID del empleado.
            
        Returns:
            Diccionario con datos del empleado o None si no existe.
        """
        pass

    @abstractmethod
    def obtener_por_correo(self, correo: str) -> Optional[dict]:
        """Obtiene un empleado por correo.
        
        Args:
            correo: Correo electrónico del empleado.
            
        Returns:
            Diccionario con datos del empleado o None si no existe.
        """
        pass

    @abstractmethod
    def listar_todos(self) -> List[dict]:
        """Lista todos los empleados.
        
        Returns:
            Lista de diccionarios con datos de empleados.
        """
        pass

    @abstractmethod
    def existe(self, empleado_id: int) -> bool:
        """Verifica si existe un empleado con el ID especificado.
        
        Args:
            empleado_id: ID del empleado.
            
        Returns:
            True si existe, False en caso contrario.
        """
        pass
