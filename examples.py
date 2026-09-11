"""
Ejemplos de uso de la API del Sistema de Gestión de Tareas.

Este script demuestra cómo consumir los endpoints usando la librería 'requests'.
Para ejecutar: python examples.py

Requiere: pip install requests
"""

import requests
import json
from typing import Dict, Any

# Configuración
BASE_URL = "http://127.0.0.1:8000/api/v1"


def print_response(title: str, response: requests.Response):
    """Imprime la respuesta de forma legible."""
    print(f"\n{'='*70}")
    print(f" {title}")
    print(f"{'='*70}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")


def ejemplo_crear_empleados():
    """Ejemplo 1: Crear empleados."""
    print("\n\n" + "#"*70)
    print("# EJEMPLO 1: CREAR EMPLEADOS")
    print("#"*70)
    
    empleados_data = [
        {
            "nombre": "Juan García",
            "correo": "juan.garcia@empresa.com",
            "cargo": "Desarrollador Senior"
        },
        {
            "nombre": "María López",
            "correo": "maria.lopez@empresa.com",
            "cargo": "Product Manager"
        },
        {
            "nombre": "Carlos Rodríguez",
            "correo": "carlos.rodriguez@empresa.com",
            "cargo": "QA Engineer"
        }
    ]
    
    empleados_creados = []
    for emp in empleados_data:
        response = requests.post(f"{BASE_URL}/empleados", json=emp)
        print_response(f"Registrando empleado: {emp['nombre']}", response)
        if response.status_code == 201:
            empleados_creados.append(response.json())
    
    return empleados_creados


def ejemplo_listar_empleados():
    """Ejemplo 2: Listar empleados."""
    print("\n\n" + "#"*70)
    print("# EJEMPLO 2: LISTAR EMPLEADOS")
    print("#"*70)
    
    response = requests.get(f"{BASE_URL}/empleados")
    print_response("Listando todos los empleados", response)
    return response.json() if response.status_code == 200 else []


def ejemplo_crear_tareas(empleados: list):
    """Ejemplo 3: Crear tareas (con y sin asignación inicial)."""
    print("\n\n" + "#"*70)
    print("# EJEMPLO 3: CREAR TAREAS")
    print("#"*70)
    
    tareas_data = [
        {
            "titulo": "Implementar autenticación JWT",
            "descripcion": "Agregar soporte de JWT al endpoint /login",
            "fecha_limite": "2024-12-31",
            "estado": "Pendiente",
            "empleado_id": empleados[0]["id"] if empleados else None
        },
        {
            "titulo": "Revisar documentación API",
            "descripcion": "Verificar que toda la documentación esté actualizada",
            "fecha_limite": "2024-12-25",
            "estado": "En proceso",
            "empleado_id": empleados[1]["id"] if len(empleados) > 1 else None
        },
        {
            "titulo": "Testing de endpoints",
            "descripcion": None,
            "fecha_limite": "2024-12-20",
            "estado": "Pendiente",
            "empleado_id": None  # Sin asignación inicial
        }
    ]
    
    tareas_creadas = []
    for idx, tarea in enumerate(tareas_data, 1):
        response = requests.post(f"{BASE_URL}/tareas", json=tarea)
        print_response(f"Creando tarea {idx}: {tarea['titulo']}", response)
        if response.status_code == 201:
            tareas_creadas.append(response.json())
    
    return tareas_creadas


def ejemplo_listar_tareas_con_responsable():
    """Ejemplo 4: Listar tareas con información del responsable (JOIN)."""
    print("\n\n" + "#"*70)
    print("# EJEMPLO 4: LISTAR TAREAS (CON RESPONSABLE)")
    print("#"*70)
    
    response = requests.get(f"{BASE_URL}/tareas")
    print_response("Listando tareas con información del responsable", response)
    return response.json() if response.status_code == 200 else []


def ejemplo_asignar_tarea(tareas: list, empleados: list):
    """Ejemplo 5: Asignar/reasignar tarea a empleado."""
    print("\n\n" + "#"*70)
    print("# EJEMPLO 5: ASIGNAR/REASIGNAR TAREA")
    print("#"*70)
    
    if not tareas or not empleados or len(empleados) < 3:
        print("No hay suficientes tareas o empleados para demostrar la asignación.")
        return
    
    # Asignar la tercera tarea al tercer empleado
    tarea_id = tareas[2]["id"]
    empleado_id = empleados[2]["id"]
    
    payload = {"empleado_id": empleado_id}
    response = requests.put(f"{BASE_URL}/tareas/{tarea_id}/asignar", json=payload)
    print_response(f"Asignando tarea {tarea_id} a empleado {empleado_id}", response)


def ejemplo_errores():
    """Ejemplo 6: Manejo de errores."""
    print("\n\n" + "#"*70)
    print("# EJEMPLO 6: MANEJO DE ERRORES")
    print("#"*70)
    
    # Error 1: Correo duplicado (409 Conflict)
    print("\n--- Error 1: Registrar empleado con correo duplicado ---")
    empleado = {
        "nombre": "Juan García",
        "correo": "juan.garcia@empresa.com",  # Ya existe
        "cargo": "Desarrollador"
    }
    response = requests.post(f"{BASE_URL}/empleados", json=empleado)
    print_response("Intento de registrar correo duplicado", response)
    
    # Error 2: Empleado no existe (404 Not Found)
    print("\n--- Error 2: Crear tarea con empleado inexistente ---")
    tarea = {
        "titulo": "Tarea de prueba",
        "fecha_limite": "2024-12-31",
        "empleado_id": 9999  # No existe
    }
    response = requests.post(f"{BASE_URL}/tareas", json=tarea)
    print_response("Intento de crear tarea con empleado inexistente", response)
    
    # Error 3: Datos inválidos (400 Bad Request)
    print("\n--- Error 3: Crear tarea con fecha inválida ---")
    tarea = {
        "titulo": "Tarea de prueba",
        "fecha_limite": "31-12-2024",  # Formato incorrecto
        "estado": "Pendiente"
    }
    response = requests.post(f"{BASE_URL}/tareas", json=tarea)
    print_response("Intento de crear tarea con fecha inválida", response)
    
    # Error 4: Estado inválido (400 Bad Request)
    print("\n--- Error 4: Crear tarea con estado inválido ---")
    tarea = {
        "titulo": "Tarea de prueba",
        "fecha_limite": "2024-12-31",
        "estado": "Cancelada"  # Estado no permitido
    }
    response = requests.post(f"{BASE_URL}/tareas", json=tarea)
    print_response("Intento de crear tarea con estado inválido", response)


def main():
    """Ejecuta todos los ejemplos."""
    print("\n")
    print("*" * 70)
    print("* EJEMPLOS DE USO: SISTEMA DE GESTIÓN DE TAREAS")
    print("*" * 70)
    print(f"\nBase URL: {BASE_URL}")
    print("\nAsegúrate de que el servidor está ejecutándose:")
    print("  uvicorn app.main:app --reload")
    
    try:
        # Ejecutar ejemplos
        empleados = ejemplo_crear_empleados()
        ejemplo_listar_empleados()
        tareas = ejemplo_crear_tareas(empleados)
        ejemplo_listar_tareas_con_responsable()
        ejemplo_asignar_tarea(tareas, empleados)
        ejemplo_errores()
        
        print("\n\n" + "="*70)
        print("")
        print("Ejemplos completados. ¡Accede a http://127.0.0.1:8000/docs")
        print("para una interfaz interactiva!")
        print("")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n\n[ERROR] No se pudo conectar al servidor.")
        print("Asegúrate de ejecutar: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n\n[ERROR] {str(e)}")


if __name__ == "__main__":
    main()
