"""
Implementación de repositorio para Tareas en SQLite.

SRP: Responsabilidad única de acceso a datos.
LSP: Implementa la interfaz de forma sustituible.
ISP: Usa solo los métodos necesarios.
"""

import sqlite3
from typing import List, Optional, Dict, Any
from app.database import db_manager
from app.repositories.tarea_repository_interface import ITareaRepository


class TareaRepository(ITareaRepository):
    """Implementación de repositorio de Tareas para SQLite."""

    # Estados válidos (sincronizar con schemas.py EstadoTarea)
    ESTADOS_VALIDOS = {"Pendiente", "En proceso", "Completada"}

    def __init__(self, database_manager):
        """Inicializa el repositorio con el gestor de BD.
        
        Args:
            database_manager: Instancia de DatabaseManager.
        """
        self.db = database_manager

    def crear(self, titulo: str, descripcion: Optional[str], fecha_limite: str,
              estado: str = "Pendiente", empleado_id: Optional[int] = None) -> Dict[str, Any]:
        """Crea una tarea con validaciones de estado y empleado.
        
        Raises:
            ValueError: Si estado es inválido o empleado_id no existe.
        """
        # Validación: estado debe estar en ESTADOS_VALIDOS
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Valores permitidos: {', '.join(self.ESTADOS_VALIDOS)}")

        # Validación: si se proporciona empleado_id, debe existir
        if empleado_id is not None:
            if not self._empleado_existe(empleado_id):
                raise ValueError(f"El empleado con ID {empleado_id} no existe.")

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """INSERT INTO tareas (titulo, descripcion, fecha_limite, estado, empleado_id)
                       VALUES (?, ?, ?, ?, ?)""",
                    (titulo, descripcion, fecha_limite, estado, empleado_id)
                )
                conn.commit()
                tarea_id = cursor.lastrowid
                return self._obtener_tarea_por_id(cursor, tarea_id)
            except sqlite3.IntegrityError as e:
                conn.rollback()
                raise ValueError(f"Error de integridad: {str(e)}")

    def obtener_por_id(self, tarea_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una tarea por ID."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            return self._obtener_tarea_por_id(cursor, tarea_id)

    def listar_todas(self) -> List[Dict[str, Any]]:
        """Lista todas las tareas."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                """SELECT id, titulo, descripcion, fecha_limite, estado, empleado_id
                   FROM tareas ORDER BY id"""
            ).fetchall()
            return [self._row_to_dict(row) for row in rows]

    def listar_con_responsable(self) -> List[Dict[str, Any]]:
        """Lista tareas con JOIN a empleados (nombre y correo del responsable).
        
        Returns:
            Lista de tareas con campos adicionales: responsable_nombre, responsable_correo.
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                """SELECT 
                     t.id,
                     t.titulo,
                     t.descripcion,
                     t.fecha_limite,
                     t.estado,
                     t.empleado_id,
                     e.nombre AS responsable_nombre,
                     e.correo AS responsable_correo
                   FROM tareas t
                   LEFT JOIN empleados e ON t.empleado_id = e.id
                   ORDER BY t.id"""
            ).fetchall()
            return [self._row_to_dict(row) for row in rows]

    def asignar(self, tarea_id: int, empleado_id: int) -> Dict[str, Any]:
        """Asigna o reasigna una tarea a un empleado.
        
        Raises:
            ValueError: Si la tarea o empleado no existen.
        """
        # Validación: tarea debe existir
        if not self.existe(tarea_id):
            raise ValueError(f"La tarea con ID {tarea_id} no existe.")

        # Validación: empleado debe existir
        if not self._empleado_existe(empleado_id):
            raise ValueError(f"El empleado con ID {empleado_id} no existe.")

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE tareas SET empleado_id = ? WHERE id = ?",
                    (empleado_id, tarea_id)
                )
                conn.commit()
                return self._obtener_tarea_por_id(cursor, tarea_id)
            except sqlite3.IntegrityError as e:
                conn.rollback()
                raise ValueError(f"Error de integridad: {str(e)}")

    def existe(self, tarea_id: int) -> bool:
        """Verifica si existe una tarea con el ID especificado."""
        return self.obtener_por_id(tarea_id) is not None

    def _empleado_existe(self, empleado_id: int) -> bool:
        """Verifica si existe un empleado (helper interno)."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            result = cursor.execute(
                "SELECT 1 FROM empleados WHERE id = ?",
                (empleado_id,)
            ).fetchone()
            return result is not None

    def _obtener_tarea_por_id(self, cursor, tarea_id: int) -> Optional[Dict[str, Any]]:
        """Helper para obtener tarea por ID usando un cursor existente."""
        row = cursor.execute(
            """SELECT id, titulo, descripcion, fecha_limite, estado, empleado_id
               FROM tareas WHERE id = ?""",
            (tarea_id,)
        ).fetchone()
        return self._row_to_dict(row) if row else None

    @staticmethod
    def _row_to_dict(row) -> Optional[Dict[str, Any]]:
        """Convierte una fila de sqlite3.Row a diccionario."""
        if row is None:
            return None
        return dict(row)
