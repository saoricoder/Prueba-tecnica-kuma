"""
Servicio de Empleados - Lógica de negocio.

Validaciones de negocio:
- Correo único en la plataforma.
- Nombre y cargo son obligatorios.
- Integración con repositorio de Empleados.

SRP: Responsabilidad única.
DIP: Recibe repositorio inyectado.
"""

from typing import List, Dict, Any, Optional
from app.repositories.empleado_repository_interface import IEmpleadoRepository


class EmpleadoService:
    """Servicio de negocio para Empleados."""

    def __init__(self, empleado_repository: IEmpleadoRepository):
        """Inicializa el servicio con repositorio inyectado.
        
        Args:
            empleado_repository: Implementación de IEmpleadoRepository.
        """
        self.empleado_repository = empleado_repository

    def registrar_empleado(self, nombre: str, correo: str, cargo: str) -> Dict[str, Any]:
        """Registra un empleado con validaciones de negocio.
        
        Validaciones:
        - Nombre no vacío.
        - Correo válido y único.
        - Cargo no vacío.
        
        Args:
            nombre: Nombre del empleado.
            correo: Correo electrónico.
            cargo: Cargo del empleado.
            
        Returns:
            Diccionario con datos del empleado creado.
            
        Raises:
            ValueError: Si los datos son inválidos o correo duplicado.
        """
        # Validación de negocio: campos obligatorios
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del empleado es obligatorio.")
        
        if not cargo or not cargo.strip():
            raise ValueError("El cargo del empleado es obligatorio.")
        
        # Normalizar espacios
        nombre = nombre.strip()
        correo = correo.strip().lower()
        cargo = cargo.strip()
        
        # Validación de negocio: unicidad de correo (verificar aquí también por seguridad)
        if self.empleado_repository.obtener_por_correo(correo) is not None:
            raise ValueError(f"El correo '{correo}' ya está registrado en la plataforma.")
        
        # Crear mediante repositorio
        return self.empleado_repository.crear(nombre, correo, cargo)

    def obtener_empleado(self, empleado_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un empleado por ID.
        
        Args:
            empleado_id: ID del empleado.
            
        Returns:
            Datos del empleado o None si no existe.
        """
        return self.empleado_repository.obtener_por_id(empleado_id)

    def listar_empleados(self) -> List[Dict[str, Any]]:
        """Lista todos los empleados registrados.
        
        Returns:
            Lista de empleados.
        """
        return self.empleado_repository.listar_todos()

    def verificar_existencia(self, empleado_id: int) -> bool:
        """Verifica si un empleado existe.
        
        Args:
            empleado_id: ID del empleado.
            
        Returns:
            True si existe, False en caso contrario.
        """
        return self.empleado_repository.existe(empleado_id)
