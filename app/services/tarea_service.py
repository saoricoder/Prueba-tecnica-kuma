"""
Servicio de Tareas - Lógica de negocio.

Validaciones de negocio:
- Estados restringidos: 'Pendiente', 'En proceso', 'Completada'.
- Empleado responsable debe existir en BD.
- Fecha límite en formato ISO YYYY-MM-DD.
- Título y fecha límite obligatorios.
- Integración con repositorio de Tareas y Empleados.

SRP: Responsabilidad única.
DIP: Recibe repositorios inyectados.
"""

from typing import List, Dict, Any, Optional
from datetime import date
from app.repositories.tarea_repository_interface import ITareaRepository
from app.repositories.empleado_repository_interface import IEmpleadoRepository


class TareaService:
    """Servicio de negocio para Tareas."""

    # Estados válidos (sincronizar con TareaRepository y schemas.py)
    ESTADOS_VALIDOS = {"Pendiente", "En proceso", "Completada"}

    def __init__(self, tarea_repository: ITareaRepository, 
                 empleado_repository: IEmpleadoRepository):
        """Inicializa el servicio con repositorios inyectados.
        
        Args:
            tarea_repository: Implementación de ITareaRepository.
            empleado_repository: Implementación de IEmpleadoRepository.
        """
        self.tarea_repository = tarea_repository
        self.empleado_repository = empleado_repository

    def crear_tarea(self, titulo: str, descripcion: Optional[str], 
                   fecha_limite: str, estado: str = "Pendiente",
                   empleado_id: Optional[int] = None) -> Dict[str, Any]:
        """Crea una tarea con validaciones de negocio.
        
        Validaciones:
        - Título no vacío.
        - Fecha límite en formato ISO YYYY-MM-DD.
        - Estado en estados válidos.
        - Si se proporciona empleado_id, debe existir.
        
        Args:
            titulo: Título de la tarea.
            descripcion: Descripción opcional.
            fecha_limite: Fecha límite en formato ISO YYYY-MM-DD.
            estado: Estado inicial (default: 'Pendiente').
            empleado_id: ID del empleado responsable (opcional).
            
        Returns:
            Diccionario con datos de la tarea creada.
            
        Raises:
            ValueError: Si los datos son inválidos.
        """
        # Validación de negocio: título obligatorio
        if not titulo or not titulo.strip():
            raise ValueError("El título de la tarea es obligatorio.")
        
        # Normalizar
        titulo = titulo.strip()
        if descripcion:
            descripcion = descripcion.strip()
        
        # Validación de negocio: fecha límite en formato válido
        try:
            fecha_obj = date.fromisoformat(fecha_limite)
        except (ValueError, TypeError):
            raise ValueError("Formato de fecha límite inválido. Esperado: YYYY-MM-DD")
        
        # Validación de negocio: estado en valores permitidos
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Estados permitidos: {', '.join(self.ESTADOS_VALIDOS)}")
        
        # Validación de negocio: si hay empleado_id, debe existir
        if empleado_id is not None:
            if not self.empleado_repository.existe(empleado_id):
                raise ValueError(f"El empleado con ID {empleado_id} no existe.")
        
        # Crear mediante repositorio
        return self.tarea_repository.crear(titulo, descripcion, fecha_limite, estado, empleado_id)

    def obtener_tarea(self, tarea_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una tarea por ID.
        
        Args:
            tarea_id: ID de la tarea.
            
        Returns:
            Datos de la tarea o None si no existe.
        """
        return self.tarea_repository.obtener_por_id(tarea_id)

    def listar_tareas(self) -> List[Dict[str, Any]]:
        """Lista todas las tareas.
        
        Returns:
            Lista de tareas.
        """
        return self.tarea_repository.listar_todas()

    def listar_tareas_con_responsable(self) -> List[Dict[str, Any]]:
        """Lista tareas con información del empleado responsable (JOIN).
        
        Returns:
            Lista de tareas con campos: responsable_nombre, responsable_correo.
        """
        return self.tarea_repository.listar_con_responsable()

    def asignar_tarea(self, tarea_id: int, empleado_id: int) -> Dict[str, Any]:
        """Asigna o reasigna una tarea a un empleado.
        
        Validaciones:
        - La tarea debe existir.
        - El empleado debe existir.
        
        Args:
            tarea_id: ID de la tarea.
            empleado_id: ID del empleado responsable.
            
        Returns:
            Diccionario con datos de la tarea actualizada.
            
        Raises:
            ValueError: Si la tarea o empleado no existen.
        """
        # Validación: tarea debe existir
        if not self.tarea_repository.existe(tarea_id):
            raise ValueError(f"La tarea con ID {tarea_id} no existe.")
        
        # Validación: empleado debe existir
        if not self.empleado_repository.existe(empleado_id):
            raise ValueError(f"El empleado con ID {empleado_id} no existe.")
        
        # Asignar mediante repositorio
        return self.tarea_repository.asignar(tarea_id, empleado_id)

    def verificar_existencia_tarea(self, tarea_id: int) -> bool:
        """Verifica si una tarea existe.
        
        Args:
            tarea_id: ID de la tarea.
            
        Returns:
            True si existe, False en caso contrario.
        """
        return self.tarea_repository.existe(tarea_id)
