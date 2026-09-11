from contextlib import contextmanager
import sqlite3

DB_NAME = "gestion_tareas.db"


class DatabaseManager:
  """Responsabilidad Única (SRP): Manejo de la conexión y esquema de BD."""

  def __init__(self, db_name: str = DB_NAME):
    self.db_name = db_name

  @contextmanager
  def get_connection(self):
    conn = sqlite3.connect(self.db_name)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
      yield conn
    finally:
      conn.close()

  def initialize_tables(self):
    with self.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT NOT NULL UNIQUE,
                    cargo TEXT NOT NULL
                )
            """)
      cursor.execute("""
                CREATE TABLE IF NOT EXISTS tareas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descripcion TEXT,
                    fecha_limite TEXT NOT NULL,
                    estado TEXT CHECK(estado IN ('Pendiente', 'En proceso', 'Completada')) DEFAULT 'Pendiente',
                    empleado_id INTEGER,
                    FOREIGN KEY (empleado_id) REFERENCES empleados (id) ON DELETE SET NULL
                )
            """)
      conn.commit()


db_manager = DatabaseManager()
