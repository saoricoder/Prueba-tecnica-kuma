#!/usr/bin/env python
"""
Script para resetear la base de datos y cargar datos de prueba.

Este script elimina el archivo de BD existente y lo reinicializa con
datos de ejemplo para testing.

Uso: python reset_db.py
"""

import os
from app.database import db_manager


def reset_database():
    """Elimina y reinicializa la base de datos."""
    db_path = db_manager.db_name
    
    # Eliminar BD existente
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"[✓] Base de datos eliminada: {db_path}")
    
    # Reinicializar tablas
    db_manager.initialize_tables()
    print(f"[✓] Base de datos reinicializada: {db_path}")
    
    # Cargar datos de prueba
    load_sample_data()
    print("[✓] Datos de prueba cargados")


def load_sample_data():
    """Carga datos de ejemplo en la BD."""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Insertar empleados
        empleados = [
            ("Juan García", "juan.garcia@empresa.com", "Desarrollador Senior"),
            ("María López", "maria.lopez@empresa.com", "Product Manager"),
            ("Carlos Rodríguez", "carlos.rodriguez@empresa.com", "QA Engineer"),
            ("Ana Martínez", "ana.martinez@empresa.com", "DevOps Engineer"),
        ]
        
        cursor.executemany(
            "INSERT INTO empleados (nombre, correo, cargo) VALUES (?, ?, ?)",
            empleados
        )
        print(f"  - {len(empleados)} empleados insertados")
        
        # Insertar tareas
        tareas = [
            ("Implementar autenticación JWT", "Agregar JWT al endpoint /login", "2024-12-31", "Pendiente", 1),
            ("Revisar documentación API", "Verificar documentación esté actualizada", "2024-12-25", "En proceso", 2),
            ("Testing de endpoints", None, "2024-12-20", "Pendiente", None),
            ("Optimizar consultas BD", "Revisar índices de la BD", "2024-12-28", "Completada", 4),
            ("Crear reportes mensuales", None, "2025-01-15", "Pendiente", None),
        ]
        
        cursor.executemany(
            """INSERT INTO tareas (titulo, descripcion, fecha_limite, estado, empleado_id)
               VALUES (?, ?, ?, ?, ?)""",
            tareas
        )
        print(f"  - {len(tareas)} tareas insertadas")
        
        conn.commit()


if __name__ == "__main__":
    print("\n" + "="*70)
    print(" RESETEAR BASE DE DATOS")
    print("="*70 + "\n")
    
    reset_database()
    
    print("\n" + "="*70)
    print(" ¡Listo! Base de datos reinicializada con datos de prueba")
    print("="*70 + "\n")
