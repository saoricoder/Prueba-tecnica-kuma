from typing import Any, Dict, List, Optional
from app.database import DatabaseManager, db_manager
from app.repositories.interfaces import IEmpleadoRepository, ITareaRepository


class SQLiteEmpleadoRepository(IEmpleadoRepository):

  def __init__(self, manager: DatabaseManager = db_manager):
    self.manager = manager

  def create(self, nombre: str, correo: str, cargo: str) -> int:
    with self.manager.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO empleados (nombre, correo, cargo) VALUES (?, ?, ?)",
          (nombre, correo, cargo),
      )
      conn.commit()
      return cursor.lastrowid

  def get_all(self) -> List[Dict[str, Any]]:
    with self.manager.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute(
          "SELECT id, nombre, correo, cargo FROM empleados ORDER BY id DESC"
      )
      return [dict(row) for row in cursor.fetchall()]

  def get_by_id(self, empleado_id: int) -> Optional[Dict[str, Any]]:
    with self.manager.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute(
          "SELECT id, nombre, correo, cargo FROM empleados WHERE id = ?",
          (empleado_id,),
      )
      row = cursor.fetchone()
      return dict(row) if row else None

  def get_by_email(self, correo: str) -> Optional[Dict[str, Any]]:
    with self.manager.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute(
          "SELECT id, nombre, correo, cargo FROM empleados WHERE correo = ?",
          (correo,),
      )
      row = cursor.fetchone()
      return dict(row) if row else None


class SQLiteTareaRepository(ITareaRepository):

  def __init__(self, manager: DatabaseManager = db_manager):
    self.manager = manager

  def create(
      self,
      titulo: str,
      descripcion: Optional[str],
      fecha_limite: str,
      estado: str,
      empleado_id: Optional[int],
  ) -> int:
    with self.manager.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute(
          """
                INSERT INTO tareas (titulo, descripcion, fecha_limite, estado, empleado_id)
                VALUES (?, ?, ?, ?, ?)
            """,
          (titulo, descripcion, fecha_limite, estado, empleado_id),
      )
      conn.commit()
      return cursor.lastrowid

  def get_all(self) -> List[Dict[str, Any]]:
    with self.manager.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute("""
                SELECT 
                    t.id, t.titulo, t.descripcion, t.fecha_limite, t.estado, 
                    t.empleado_id, e.nombre AS responsable_nombre, e.correo AS responsable_correo
                FROM tareas t
                LEFT JOIN empleados e ON t.empleado_id = e.id
                ORDER BY t.id DESC
            """)
      return [dict(row) for row in cursor.fetchall()]

  def get_by_id(self, tarea_id: int) -> Optional[Dict[str, Any]]:
    with self.manager.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,))
      row = cursor.fetchone()
      return dict(row) if row else None

  def assign_employee(self, tarea_id: int, empleado_id: int) -> bool:
    with self.manager.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute(
          "UPDATE tareas SET empleado_id = ? WHERE id = ?",
          (empleado_id, tarea_id),
      )
      conn.commit()
      return cursor.rowcount > 0
