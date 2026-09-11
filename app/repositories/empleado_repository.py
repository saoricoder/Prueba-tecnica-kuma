"""
Implementación de repositorio para Empleados en SQLite.

SRP: Responsabilidad única de acceso a datos.
LSP: Implementa la interfaz de forma sustituible.
ISP: Usa solo los métodos necesarios.
"""

import sqlite3
from typing import List, Optional, Dict, Any
from app.database import db_manager
from app.repositories.empleado_repository_interface import IEmpleadoRepository


class EmpleadoRepository(IEmpleadoRepository):
    """Implementación de repositorio de Empleados para SQLite."""

    def __init__(self, database_manager):
        """Inicializa el repositorio con el gestor de BD.
        
        Args:
            database_manager: Instancia de DatabaseManager.
        """
        self.db = database_manager

    def crear(self, nombre: str, correo: str, cargo: str) -> Dict[str, Any]:
        """Crea un empleado con validación de unicidad de correo.
        
        Raises:
            ValueError: Si el correo ya existe.
        """
        # Validación: verificar que el correo no exista
        if self.obtener_por_correo(correo) is not None:
            raise ValueError(f"El correo '{correo}' ya está registrado.")

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO empleados (nombre, correo, cargo) VALUES (?, ?, ?)",
                    (nombre, correo, cargo)
                )
                conn.commit()
                empleado_id = cursor.lastrowid
                return self._row_to_dict(cursor.execute(
                    "SELECT id, nombre, correo, cargo FROM empleados WHERE id = ?",
                    (empleado_id,)
                ).fetchone())
            except sqlite3.IntegrityError as e:
                conn.rollback()
                raise ValueError(f"Error de integridad: {str(e)}")

    def obtener_por_id(self, empleado_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un empleado por ID."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(
                "SELECT id, nombre, correo, cargo FROM empleados WHERE id = ?",
                (empleado_id,)
            ).fetchone()
            return self._row_to_dict(row) if row else None

    def obtener_por_correo(self, correo: str) -> Optional[Dict[str, Any]]:
        """Obtiene un empleado por correo."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(
                "SELECT id, nombre, correo, cargo FROM empleados WHERE correo = ?",
                (correo,)
            ).fetchone()
            return self._row_to_dict(row) if row else None

    def listar_todos(self) -> List[Dict[str, Any]]:
        """Lista todos los empleados."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                "SELECT id, nombre, correo, cargo FROM empleados ORDER BY id"
            ).fetchall()
            return [self._row_to_dict(row) for row in rows]

    def existe(self, empleado_id: int) -> bool:
        """Verifica si existe un empleado con el ID especificado."""
        return self.obtener_por_id(empleado_id) is not None

    @staticmethod
    def _row_to_dict(row) -> Optional[Dict[str, Any]]:
        """Convierte una fila de sqlite3.Row a diccionario."""
        if row is None:
            return None
        return dict(row)
