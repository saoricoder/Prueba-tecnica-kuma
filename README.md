# Sistema de Gestión de Tareas (FastAPI + SQLite)

Solución técnica para la gestión de empleados y asignación de tareas implementada bajo arquitectura por capas (**MVC**) y principios **SOLID**.

## Arquitectura y Principios SOLID

1. **SRP (Responsabilidad Única):** Clases separadas para acceso a datos, lógica de negocio, persistencia y enrutamiento.
2. **OCP (Abierto/Cerrado):** Extensible a nuevos motores de BD sin modificar la lógica existente.
3. **LSP (Sustitución de Liskov):** Repositorios intercambiables.
4. **ISP (Segregación de Interfaces):** Interfaces específicas y desacopladas.
5. **DIP (Inversión de Dependencias):** Inyección de dependencias mediante FastAPI Depends().

## Ejecución Local

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Acceso:**
- API Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| POST | /empleados | Registrar empleado |
| GET | /empleados | Listar empleados |
| POST | /tareas | Crear tarea |
| GET | /tareas | Listar tareas |
| PUT | /tareas/{id}/asignar | Asignar tarea |

## Despliegue

**Backend:** Render / Railway  
**Frontend:** GitHub Pages

Autor: Prueba Técnica KUMA | v1.0.0
