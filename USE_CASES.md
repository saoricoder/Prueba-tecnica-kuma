# Casos de Uso - Sistema de Gestión de Tareas

## 📄 Descripción General

Este documento describe los casos de uso principales del Sistema de Gestión de Tareas, incluyendo actores, precondiciones, flujos principales y alternos.

---

## 👤 Actores

1. **Administrador**: Gestiona empleados y tareas
2. **Empleado**: Realiza tareas asignadas (v1.0.0: solo lectura)

---

## 🔍 Casos de Uso

### CU-01: Registrar Empleado

**Objetivo**: Crear un nuevo empleado en el sistema.

**Actor Principal**: Administrador

**Precondiciones**:
- El correo no existe en la BD
- La aplicación está activa

**Flujo Principal**:
1. Administrador solicita crear empleado
2. Sistema valida datos (nombre, correo, cargo)
3. Sistema verifica unicidad de correo
4. Sistema almacena empleado en BD
5. Sistema retorna ID asignado (201 Created)

**Flujo Alternativo A: Correo Duplicado**
1. En paso 3: correo ya existe
2. Sistema retorna error 409 Conflict
3. Caso de uso termina

**Flujo Alternativo B: Datos Inválidos**
1. En paso 2: nombre o cargo vacíos, o email mal formado
2. Sistema retorna error 400 Bad Request
3. Caso de uso termina

**Datos de Entrada**:
```json
{
  "nombre": "Juan García",
  "correo": "juan.garcia@empresa.com",
  "cargo": "Desarrollador Senior"
}
```

**Datos de Salida**:
```json
{
  "id": 1,
  "nombre": "Juan García",
  "correo": "juan.garcia@empresa.com",
  "cargo": "Desarrollador Senior"
}
```

**Status Code**: 201 Created

---

### CU-02: Listar Empleados

**Objetivo**: Consultar todos los empleados registrados.

**Actor Principal**: Administrador, Empleado

**Precondiciones**:
- La aplicación está activa
- Existen empleados en BD (opcional)

**Flujo Principal**:
1. Actor solicita listar empleados
2. Sistema obtiene todos los empleados de BD
3. Sistema retorna lista de empleados (200 OK)

**Datos de Salida**:
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

**Status Code**: 200 OK

---

### CU-03: Crear Tarea

**Objetivo**: Crear una nueva tarea con asignación opcional.

**Actor Principal**: Administrador

**Precondiciones**:
- La aplicación está activa
- Si se asigna, el empleado debe existir

**Flujo Principal**:
1. Administrador solicita crear tarea
2. Sistema valida datos (título, fecha límite, estado)
3. Sistema verifica que estado esté en valores permitidos
4. Si hay empleado_id, verifica que empleado existe
5. Sistema almacena tarea en BD
6. Sistema retorna ID asignado (201 Created)

**Flujo Alternativo A: Empleado No Existe**
1. En paso 4: empleado_id no encontrado
2. Sistema retorna error 404 Not Found
3. Caso de uso termina

**Flujo Alternativo B: Estado Inválido**
1. En paso 3: estado ∉ {"Pendiente", "En proceso", "Completada"}
2. Sistema retorna error 400 Bad Request
3. Caso de uso termina

**Flujo Alternativo C: Fecha Inválida**
1. En paso 2: fecha no en formato ISO YYYY-MM-DD
2. Sistema retorna error 400 Bad Request
3. Caso de uso termina

**Datos de Entrada**:
```json
{
  "titulo": "Implementar autenticación JWT",
  "descripcion": "Agregar JWT al endpoint /login",
  "fecha_limite": "2024-12-31",
  "estado": "Pendiente",
  "empleado_id": 1
}
```

**Datos de Salida**:
```json
{
  "id": 1,
  "titulo": "Implementar autenticación JWT",
  "descripcion": "Agregar JWT al endpoint /login",
  "fecha_limite": "2024-12-31",
  "estado": "Pendiente",
  "empleado_id": 1
}
```

**Status Code**: 201 Created

---

### CU-04: Listar Tareas con Responsable

**Objetivo**: Consultar todas las tareas con información del empleado responsable (JOIN).

**Actor Principal**: Administrador, Empleado

**Precondiciones**:
- La aplicación está activa
- Existen tareas en BD (opcional)

**Flujo Principal**:
1. Actor solicita listar tareas
2. Sistema ejecuta JOIN entre tareas y empleados
3. Sistema retorna lista de tareas con datos del responsable (200 OK)

**Notas**:
- Si una tarea no está asignada: `responsable_nombre` y `responsable_correo` son `null`
- Si empleado fue eliminado: campos del responsable quedan `null`

**Datos de Salida**:
```json
[
  {
    "id": 1,
    "titulo": "Implementar autenticación JWT",
    "descripcion": "Agregar JWT al endpoint /login",
    "fecha_limite": "2024-12-31",
    "estado": "Pendiente",
    "empleado_id": 1,
    "responsable_nombre": "Juan García",
    "responsable_correo": "juan.garcia@empresa.com"
  },
  {
    "id": 2,
    "titulo": "Testing de endpoints",
    "descripcion": null,
    "fecha_limite": "2024-12-20",
    "estado": "En proceso",
    "empleado_id": null,
    "responsable_nombre": null,
    "responsable_correo": null
  }
]
```

**Status Code**: 200 OK

---

### CU-05: Asignar Tarea a Empleado

**Objetivo**: Asignar o reasignar una tarea existente a un empleado existente.

**Actor Principal**: Administrador

**Precondiciones**:
- La aplicación está activa
- La tarea debe existir
- El empleado debe existir

**Flujo Principal**:
1. Administrador solicita asignar tarea a empleado
2. Sistema verifica que tarea existe
3. Sistema verifica que empleado existe
4. Sistema actualiza campo `empleado_id` de la tarea
5. Sistema retorna tarea actualizada (200 OK)

**Flujo Alternativo A: Tarea No Existe**
1. En paso 2: tarea_id no encontrado
2. Sistema retorna error 404 Not Found
3. Caso de uso termina

**Flujo Alternativo B: Empleado No Existe**
1. En paso 3: empleado_id no encontrado
2. Sistema retorna error 404 Not Found
3. Caso de uso termina

**Datos de Entrada**:
```json
{
  "empleado_id": 2
}
```

**Datos de Salida**:
```json
{
  "id": 1,
  "titulo": "Implementar autenticación JWT",
  "descripcion": "Agregar JWT al endpoint /login",
  "fecha_limite": "2024-12-31",
  "estado": "Pendiente",
  "empleado_id": 2
}
```

**Status Code**: 200 OK

**Nota**: Esta acción permite reasignar una tarea ya existente a un empleado diferente.

---

## 📊 Matriz de Cobertura de Endpoints

| Caso de Uso | Método | Endpoint | Estado |
|-------------|--------|----------|--------|
| CU-01 | POST | /api/v1/empleados | ✅ Implementado |
| CU-02 | GET | /api/v1/empleados | ✅ Implementado |
| CU-03 | POST | /api/v1/tareas | ✅ Implementado |
| CU-04 | GET | /api/v1/tareas | ✅ Implementado |
| CU-05 | PUT | /api/v1/tareas/{id}/asignar | ✅ Implementado |

---

## 🐟 Extensiones Futuras

### CU-06: Actualizar Empleado (v2.0.0)
**Método**: PUT /api/v1/empleados/{id}
- Permitir modificar nombre, cargo
- Validar unicidad de correo

### CU-07: Eliminar Empleado (v2.0.0)
**Método**: DELETE /api/v1/empleados/{id}
- Verificar si tiene tareas asignadas
- Opcionalmente: cascade delete o SET NULL

### CU-08: Actualizar Tarea (v2.0.0)
**Método**: PUT /api/v1/tareas/{id}
- Modificar título, descripción, estado, fecha límite
- Validaciones de negocio

### CU-09: Eliminar Tarea (v2.0.0)
**Método**: DELETE /api/v1/tareas/{id}
- Soft delete (marcar como eliminado)
- O hard delete (remover completamente)

### CU-10: Filtrar Tareas por Estado (v2.0.0)
**Método**: GET /api/v1/tareas?estado=Pendiente
- Buscar tareas por estado
- Paginación

### CU-11: Autenticación y Autorización (v2.0.0)
**Método**: POST /api/v1/auth/login
- OAuth2 con JWT
- Roles: Admin, Manager, Employee
- Proteger endpoints sensibles

---

## 📄 Especificación de Errores

### 400 Bad Request
Datos de entrada inválidos o faltantes.

**Ejemplos**:
- Campo requerido faltante
- Tipo de dato incorrecto
- Valor fuera de rango permitido
- Formato de fecha inválido
- Estado no permitido

**Response**:
```json
{
  "detail": "El título de la tarea es obligatorio."
}
```

### 404 Not Found
Recurso no encontrado en BD.

**Ejemplos**:
- Empleado con ID 999 no existe
- Tarea con ID 999 no existe

**Response**:
```json
{
  "detail": "La tarea con ID 999 no existe."
}
```

### 409 Conflict
Violación de restricción única o integridad referencial.

**Ejemplos**:
- Correo de empleado ya registrado
- Violación de UNIQUE constraint

**Response**:
```json
{
  "detail": "El correo 'juan.garcia@empresa.com' ya está registrado en la plataforma."
}
```

### 500 Internal Server Error
Error no esperado en el servidor.

**Response**:
```json
{
  "detail": "Error interno al crear empleado"
}
```

---

## 📚 Flujo de Negocio Completo

### Escenario: Crear Tarea y Asignar a Empleado

**Paso 1**: Registrar empleado
```bash
curl -X POST http://localhost:8000/api/v1/empleados \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan","correo":"juan@empresa.com","cargo":"Dev"}'
# Response: {"id": 1, ...}
```

**Paso 2**: Crear tarea sin asignación
```bash
curl -X POST http://localhost:8000/api/v1/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Tarea 1","fecha_limite":"2024-12-31","estado":"Pendiente"}'
# Response: {"id": 1, "empleado_id": null, ...}
```

**Paso 3**: Asignar tarea al empleado
```bash
curl -X PUT http://localhost:8000/api/v1/tareas/1/asignar \
  -H "Content-Type: application/json" \
  -d '{"empleado_id": 1}'
# Response: {"id": 1, "empleado_id": 1, ...}
```

**Paso 4**: Verificar tarea con responsable
```bash
curl http://localhost:8000/api/v1/tareas
# Response: [{"id": 1, "empleado_id": 1, "responsable_nombre": "Juan", ...}]
```

---

## 🧪 Testing de Casos de Uso

### Con Swagger UI
1. http://localhost:8000/docs
2. Expandir cada endpoint
3. Click "Try it out"
4. Ingresar datos de prueba
5. Ejecutar y verificar respuesta

### Con Script Python
Ver `examples.py` para scripts de prueba automática.

### Con cURL
Ejémplos incluidos en `README.md`.

---
