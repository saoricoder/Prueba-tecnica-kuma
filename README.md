# Sistema de Gestión de Tareas (FastAPI + SQLite)

**Solución técnica de gestión de empleados y asignación de tareas** implementada bajo arquitectura por capas (**MVC**) y principios **SOLID** con tipado estricto, validación automática y documentación interactiva.

---

## 📋 Tabla de Contenidos

1. [Justificación del Stack](#justificación-del-stack)
2. [Arquitectura y Principios SOLID](#arquitectura-y-principios-solid)
3. [Modelo de Datos](#modelo-de-datos)
4. [Catálogo de Endpoints](#catálogo-de-endpoints)
5. [Guía de Inicio Rápido](#guía-de-inicio-rápido)
6. [Despliegue en GitHub Codespaces](#despliegue-en-github-codespaces)
7. [Estructura del Proyecto](#estructura-del-proyecto)

---

## 🏗️ Justificación del Stack

### Python 3.10+

- **Tipado Estricto**: Soporte nativo para type hints que mejora legibilidad, mantenibilidad y detección de errores en tiempo de desarrollo.
- **Productividad**: Sintaxis clara y expresiva para implementar lógica de negocio compleja de forma concisa.
- **Ecosistema Maduro**: Librerías de calidad empresarial para validación, ORM, testing y más.

### FastAPI

- **Velocidad de Ejecución**: Framework ASGI moderno, significativamente más rápido que Django y comparable a Node.js/Go.
- **Tipado Automático**: Integración nativa con Pydantic para validación en tiempo de ejecución basada en type hints.
- **Documentación Interactiva**: Genera automáticamente especificación OpenAPI 3.0 con Swagger UI y ReDoc.
- **Inyección de Dependencias**: Sistema integrado (FastAPI `Depends()`) para desacoplamiento y testabilidad.
- **Manejo de Errores Robusto**: Respuestas HTTP semánticas y exception handlers centralizados.

### Pydantic v2

- **Validación de Datos**: Declara esquemas con validadores, restricciones de tipo y mensajes de error personalizados.
- **Serialización/Deserialización**: Conversión automática entre JSON y modelos Python.
- **email-validator**: Plugin para validación de direcciones de correo electrónico (RFC compliant).

### SQLite

- **Sin Dependencias Externas**: Base de datos embebida, no requiere servidor separado.
- **Transacciones ACID**: Garantiza integridad de datos con soporte para claves foráneas y constraints.
- **Suficiente para MVP**: Excelente para prototipos y aplicaciones de mediano alcance.
- **Portabilidad**: Un único archivo `.db` facilita backups y despliegue.

---

## 🎯 Arquitectura y Principios SOLID

### Estructura por Capas (MVC Adaptado)

```
app/
├── controllers/          # Capa de Presentación (HTTP endpoints)
│   ├── empleado_controller.py
│   ├── tarea_controller.py
│   └── api_routes.py
├── services/            # Capa de Lógica de Negocio
│   ├── empleado_service.py
│   └── tarea_service.py
├── repositories/        # Capa de Acceso a Datos (Repository Pattern)
│   ├── empleado_repository_interface.py
│   ├── empleado_repository.py
│   ├── tarea_repository_interface.py
│   └── tarea_repository.py
├── models/              # Esquemas de Validación (Pydantic)
│   └── schemas.py
├── database.py          # Gestor de Conexiones
└── main.py              # Punto de Entrada
```

### Principios SOLID Aplicados

| Principio | Implementación | Beneficio |
|-----------|---|---|
| **SRP** (Responsabilidad Única) | Controllers → Enrutamiento; Services → Lógica; Repositories → Datos | Código modular, fácil de testear |
| **OCP** (Abierto/Cerrado) | Interfaces abstractas (`IEmpleadoRepository`, `ITareaRepository`) | Extensible a nuevos motores de BD sin modificar código existente |
| **LSP** (Sustitución de Liskov) | Repositorios intercambiables que cumplen interfaz | Implementaciones concretas (SQLite, PostgreSQL, MongoDB) sin romper contrato |
| **ISP** (Segregación de Interfaces) | Interfaces específicas por entidad | Clientes no dependen de métodos innecesarios |
| **DIP** (Inversión de Dependencias) | Inyección via `FastAPI Depends()` | Desacoplamiento, testing con mocks simplificado |

### Flujo de Datos

```
HTTP Request
    ↓
[Controller] - Valida datos de entrada (OpenAPI)
    ↓
[Service] - Aplica lógica de negocio y validaciones
    ↓
[Repository] - Persiste en BD (SQLite) con transacciones
    ↓
HTTP Response (JSON tipado)
```

---

## 📊 Modelo de Datos

### Tabla: `empleados`

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| `nombre` | TEXT | NOT NULL | Nombre del empleado |
| `correo` | TEXT | NOT NULL, UNIQUE | Email válido (RFC) |
| `cargo` | TEXT | NOT NULL | Puesto del empleado |

**Ejemplo:**
```sql
INSERT INTO empleados (nombre, correo, cargo) 
VALUES ('Juan García', 'juan.garcia@empresa.com', 'Desarrollador Senior');
```

### Tabla: `tareas`

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| `titulo` | TEXT | NOT NULL | Título de la tarea |
| `descripcion` | TEXT | NULL | Descripción opcional |
| `fecha_limite` | TEXT | NOT NULL | Fecha ISO YYYY-MM-DD |
| `estado` | TEXT | CHECK IN ('Pendiente', 'En proceso', 'Completada'), DEFAULT 'Pendiente' | Estado actual |
| `empleado_id` | INTEGER | FK → empleados(id), ON DELETE SET NULL | Asignación (1:N) |

**Ejemplo:**
```sql
INSERT INTO tareas (titulo, descripcion, fecha_limite, estado, empleado_id) 
VALUES ('Implementar autenticación', 'Agregar JWT', '2024-12-31', 'Pendiente', 1);
```

### Relaciones

- **1 Empleado : N Tareas** (relación 1:N)
- Integridad referencial activa: `PRAGMA foreign_keys = ON`
- `ON DELETE SET NULL`: Si se elimina un empleado, sus tareas quedan sin asignación

---

## 🔌 Catálogo de Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### 1. Registrar Empleado

**Endpoint:** `POST /empleados`

**Status Codes:**
- `201 Created`: Empleado registrado exitosamente
- `400 Bad Request`: Datos inválidos
- `409 Conflict`: Correo ya registrado

**Request:**
```json
{
  "nombre": "Juan García",
  "correo": "juan.garcia@empresa.com",
  "cargo": "Desarrollador Senior"
}
```

**Response (201):**
```json
{
  "id": 1,
  "nombre": "Juan García",
  "correo": "juan.garcia@empresa.com",
  "cargo": "Desarrollador Senior"
}
```

---

### 2. Listar Empleados

**Endpoint:** `GET /empleados`

**Status Codes:**
- `200 OK`: Lista de empleados obtenida

**Response (200):**
```json
[
  {
    "id": 1,
    "nombre": "Juan García",
    "correo": "juan.garcia@empresa.com",
    "cargo": "Desarrollador Senior"
  },
  {
    "id": 2,
    "nombre": "María López",
    "correo": "maria.lopez@empresa.com",
    "cargo": "Product Manager"
  }
]
```

---

### 3. Crear Tarea

**Endpoint:** `POST /tareas`

**Status Codes:**
- `201 Created`: Tarea creada exitosamente
- `400 Bad Request`: Datos inválidos
- `404 Not Found`: Empleado no existe

**Request:**
```json
{
  "titulo": "Implementar autenticación",
  "descripcion": "Agregar JWT al endpoint /login",
  "fecha_limite": "2024-12-31",
  "estado": "Pendiente",
  "empleado_id": null
}
```

**Response (201):**
```json
{
  "id": 1,
  "titulo": "Implementar autenticación",
  "descripcion": "Agregar JWT al endpoint /login",
  "fecha_limite": "2024-12-31",
  "estado": "Pendiente",
  "empleado_id": null
}
```

---

### 4. Listar Tareas (con Responsable)

**Endpoint:** `GET /tareas`

**Status Codes:**
- `200 OK`: Lista de tareas obtenida

**Response (200):** *(JOIN a empleados)*
```json
[
  {
    "id": 1,
    "titulo": "Implementar autenticación",
    "descripcion": "Agregar JWT al endpoint /login",
    "fecha_limite": "2024-12-31",
    "estado": "Pendiente",
    "empleado_id": 1,
    "responsable_nombre": "Juan García",
    "responsable_correo": "juan.garcia@empresa.com"
  },
  {
    "id": 2,
    "titulo": "Revisar documentación",
    "descripcion": null,
    "fecha_limite": "2024-12-25",
    "estado": "En proceso",
    "empleado_id": null,
    "responsable_nombre": null,
    "responsable_correo": null
  }
]
```

---

### 5. Asignar/Reasignar Tarea

**Endpoint:** `PUT /tareas/{id}/asignar`

**Status Codes:**
- `200 OK`: Tarea asignada exitosamente
- `400 Bad Request`: Datos inválidos
- `404 Not Found`: Tarea o empleado no existe

**Request:**
```json
{
  "empleado_id": 2
}
```

**Response (200):**
```json
{
  "id": 1,
  "titulo": "Implementar autenticación",
  "descripcion": "Agregar JWT al endpoint /login",
  "fecha_limite": "2024-12-31",
  "estado": "Pendiente",
  "empleado_id": 2
}
```

---

## 🚀 Guía de Inicio Rápido

### Prerequisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Instalación Local

1. **Clonar el repositorio:**
```bash
git clone https://github.com/saoricoder/Prueba-tecnica-kuma.git
cd Prueba-tecnica-kuma
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
uvicorn app.main:app --reload
```

5. **Acceder a la API:**

| Recurso | URL |
|---------|-----|
| **API Docs (Swagger UI)** | http://127.0.0.1:8000/docs |
| **ReDoc** | http://127.0.0.1:8000/redoc |
| **Health Check** | http://127.0.0.1:8000 |
| **Empleados** | http://127.0.0.1:8000/api/v1/empleados |
| **Tareas** | http://127.0.0.1:8000/api/v1/tareas |

---

## 🐙 Despliegue en GitHub Codespaces

### Pasos

1. **Crear Codespace:**
   - Abre tu repositorio en GitHub
   - Click en **"Code"** → **"Codespaces"** → **"Create codespace on main"
   - Espera a que se inicialice el entorno (2-3 minutos)

2. **Terminal - Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar aplicación:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

4. **Acceder desde navegador:**
   - GitHub Codespaces automáticamente expone el puerto 8000
   - Hace un forward del puerto y genera una URL pública
   - Haz click en la notificación: **"Your application is available at..."**
   - O navega a: `https://[codespace-id]...github.dev:8000/docs`

### Consumo desde Frontend (index.html)

El Codespace expone el puerto 8000 públicamente. Para consumir desde un `index.html`:

```javascript
// JavaScript en frontend
const BASE_URL = 'https://[codespace-url]:8000/api/v1';

// Registrar empleado
fetch(`${BASE_URL}/empleados`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    nombre: 'Juan García',
    correo: 'juan.garcia@empresa.com',
    cargo: 'Desarrollador'
  })
})
.then(res => res.json())
.then(data => console.log('Empleado creado:', data));
```

**Nota:** CORS está habilitado con `allow_origins=["*"]`. En producción, restringir a dominios específicos.

---

## 📁 Estructura del Proyecto

```
Prueba-tecnica-kuma/
├── app/
│   ├── __init__.py
│   ├── main.py                          # Punto de entrada
│   ├── database.py                      # Gestor de BD
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py                   # Esquemas Pydantic (validación)
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── empleado_controller.py       # Endpoints de empleados
│   │   ├── tarea_controller.py          # Endpoints de tareas
│   │   └── api_routes.py                # Enrutador principal
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── empleado_service.py          # Lógica de negocio (empleados)
│   │   └── tarea_service.py             # Lógica de negocio (tareas)
│   │
│   └── repositories/
│       ├── __init__.py
│       ├── empleado_repository_interface.py    # Interfaz abstracta
│       ├── empleado_repository.py              # Implementación SQLite
│       ├── tarea_repository_interface.py       # Interfaz abstracta
│       └── tarea_repository.py                 # Implementación SQLite
│
├── gestion_tareas.db                    # Base de datos SQLite (generada)
├── requirements.txt                     # Dependencias Python
├── README.md                            # Este archivo
└── .gitignore                           # Archivos ignorados por Git
```

---

## 🧪 Testeo

### Con Swagger UI (Recomendado)

1. Ejecuta `uvicorn app.main:app --reload`
2. Abre http://127.0.0.1:8000/docs
3. Click en cada endpoint → Click en **"Try it out"** → Ingresa datos → Click en **"Execute"

### Con curl

```bash
# Registrar empleado
curl -X POST http://127.0.0.1:8000/api/v1/empleados \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan García","correo":"juan@empresa.com","cargo":"Dev"}'

# Listar empleados
curl http://127.0.0.1:8000/api/v1/empleados

# Crear tarea
curl -X POST http://127.0.0.1:8000/api/v1/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Tarea 1","fecha_limite":"2024-12-31","estado":"Pendiente"}'

# Listar tareas
curl http://127.0.0.1:8000/api/v1/tareas

# Asignar tarea
curl -X PUT http://127.0.0.1:8000/api/v1/tareas/1/asignar \
  -H "Content-Type: application/json" \
  -d '{"empleado_id":1}'
```

---

## 📝 Variables de Entorno (Futuro)

Para configuración avanzada (no incluido en v1.0.0):

```bash
# .env (crear en raíz del proyecto)
DATABASE_URL=sqlite:///gestion_tareas.db
DEBUG=True
CORS_ORIGINS=http://localhost:3000,https://frontend.com
```

---

## 🔐 Seguridad (Consideraciones para Producción)

- [ ] Agregar autenticación OAuth2 / JWT
- [ ] Implementar autorización con roles (Admin, Manager, Employee)
- [ ] Validar CORS con dominios específicos
- [ ] Usar HTTPS/TLS
- [ ] Migrar a PostgreSQL para datasets mayores
- [ ] Implementar rate limiting
- [ ] Logging centralizado
- [ ] Monitoreo y alertas

---

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [SQLite Official](https://www.sqlite.org/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [OpenAPI Specification](https://spec.openapis.org/)

---

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles.

---

**Autor:** Prueba Técnica KUMA  
**Versión:** 1.0.0  
**Última actualización:** 2026-09-11
