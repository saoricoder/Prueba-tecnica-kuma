# Arquitectura del Sistema de Gestión de Tareas

## Visión General

Esta arquitectura implementa una solución escalable y mantenible para la gestión de empleados y asignación de tareas, siguiendo los principios SOLID y patrones de diseño empresariales.

## Diagrama de Capas

```
┌───────────────────────────────┐
│  Capa de Presentación (HTTP/REST)                  │
│  - Controllers (FastAPI)
│  - Validación con Pydantic
│  - Respuestas HTTP semánticas                    │
├───────────────────────────────┤
│
│  Inyección de Dependencias (FastAPI Depends)
│
├───────────────────────────────┤
│  Capa de Lógica de Negocio (Services)           │
│  - Validaciones de dominio
│  - Orquestación de repositorios
│  - Reglas de negocio                              │
���───────────────────────────────┤
│
│  Interfaces Abstractas (Repository Pattern)
│  - DIP: Invertir dependencias
│
├───────────────────────────────┤
│  Capa de Acceso a Datos (Repositories)           │
│  - Implementación SQLite
│  - Transacciones ACID
│  - Consultas parametrizadas                       │
├───────────────────────────────┤
│
│  Capa de Base de Datos
│
└───────────────────────────────┘
```

## Flujo de Solicitud (Request-Response)

```
Cliente HTTP (cURL, Postman, Browser)
    ↓
    POST /api/v1/empleados
    {"nombre": "Juan", "correo": "juan@empresa.com", "cargo": "Dev"}
    ↓
[CONTROLLER - empleado_controller.py]
    - Recibe Request JSON
    - Valida usando Pydantic (EmpleadoCrear schema)
    - Maneja errores HTTP
    ↓
[SERVICE - empleado_service.py]
    - Valida lógica de negocio
    - Verifica unicidad de correo
    - Normaliza datos
    ↓
[REPOSITORY - empleado_repository.py]
    - Accede a base de datos
    - Ejecuta INSERT en tabla empleados
    - Retorna empleado creado
    ↓
[DATABASE - gestion_tareas.db]
    - SQLite almacena registro
    - Transacción ACID
    ↓
[Response 201 Created]
    {
      "id": 1,
      "nombre": "Juan",
      "correo": "juan@empresa.com",
      "cargo": "Dev"
    }
```

## Principios SOLID - Detalles de Implementación

### 1. SRP (Single Responsibility Principle)

**Responsabilidad Única de cada clase:**

- **Controllers**: Enrutamiento HTTP y conversión de formatos
- **Services**: Lógica de negocio y validaciones
- **Repositories**: Acceso a datos y persistencia
- **Models/Schemas**: Validación de estructura de datos
- **Database**: Gestión de conexiones

**Beneficios:**
- Código más modular y testeable
- Cambios localizados a un único lugar
- Fácil de entender y mantener

**Ejemplo:**
```python
# SRP: EmpleadoRepository sólo maneja acceso a datos
class EmpleadoRepository(IEmpleadoRepository):
    def crear(self, nombre: str, correo: str, cargo: str) -> dict:
        # Sólo persistencia, NO validación de negocio
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(...)
            conn.commit()
```

### 2. OCP (Open/Closed Principle)

**Abierto a extensión, cerrado a modificación:**

- Interfaces abstractas definen contratos
- Nuevas implementaciones sin modificar código existente
- Soporte para múltiples backends de BD

**Extensiones posibles:**
```python
# Agregar PostgreSQL sin modificar Services
class EmpleadoRepositoryPostgres(IEmpleadoRepository):
    def crear(self, nombre: str, correo: str, cargo: str) -> dict:
        # Conectar a PostgreSQL en lugar de SQLite
        ...

# El Service sigue funcionando igual
service = EmpleadoService(EmpleadoRepositoryPostgres(db))
```

### 3. LSP (Liskov Substitution Principle)

**Sustitucionalidad de implementaciones:**

- Cualquier implementación de interfaz es intercambiable
- El Service no conoce la implementación concreta
- Contrato definido por la interfaz

**Ejemplo:**
```python
class EmpleadoService:
    def __init__(self, empleado_repository: IEmpleadoRepository):
        # No importa si es SQLite, PostgreSQL, MongoDB
        # El servicio funciona igual con cualquiera
        self.empleado_repository = empleado_repository
```

### 4. ISP (Interface Segregation Principle)

**Interfaces específicas y pequeñas:**

- `IEmpleadoRepository`: Métodos para empleados
- `ITareaRepository`: Métodos para tareas
- Clientes no dependen de métodos innecesarios

**Beneficios:**
- Interfaces claras y enfocadas
- Desacoplamiento fuerte
- Fácil de documentar y entender

### 5. DIP (Dependency Inversion Principle)

**Invertir dependencias hacia abstracciones:**

- Services dependen de interfaces, NO de implementaciones concretas
- Inyección de dependencias mediante `FastAPI Depends()`
- Inversamente al código tradicional (que depende de clases concretas)

**Ejemplo:**
```python
# DIP correcto: depender de interfaz
class EmpleadoService:
    def __init__(self, repo: IEmpleadoRepository):  # Interfaz
        self.repo = repo

# Inyección en controller
def get_empleado_service() -> EmpleadoService:
    repository = EmpleadoRepository(db_manager)  # Implementación concreta
    return EmpleadoService(repository)  # Inyectar al servicio
```

## Patrón Repository

### Propósito

Abstraer la lógica de acceso a datos detrás de una interfaz común.

### Estructura

```
IEmpleadoRepository (Interfaz)
    ↑
    └── EmpleadoRepository (Implementación SQLite)
    └── EmpleadoRepositoryPostgres (Futura)
    └── EmpleadoRepositoryMongo (Futura)
```

### Beneficios

1. **Testabilidad**: Mockear repositorio en tests
2. **Flexibilidad**: Cambiar BD sin tocar servicios
3. **Separación de Concerns**: Lógica de negocio vs acceso a datos
4. **Reutilización**: Implementación compartida entre proyectos

## Inyección de Dependencias con FastAPI

### FastAPI Depends()

```python
@router.post("/empleados")
def crear_empleado(
    empleado: EmpleadoCrear,
    service: EmpleadoService = Depends(get_empleado_service)
):
    # FastAPI automáticamente:
    # 1. Crea instancia del servicio
    # 2. La inyecta en el parámetro
    # 3. La destruye al finalizar la solicitud
    ...
```

### Ventajas

- Desacoplamiento
- Fácil testing (reemplazar con mocks)
- Ciclo de vida automático
- Reutilización entre endpoints

## Modelo Relacional

### Tablas

**empleados**
```
+----------+--------+----------+--------+
| id (PK)  | nombre | correo   | cargo  |
+----------+--------+----------+--------+
| 1        | Juan   | j@e.com  | Dev    |
| 2        | María | m@e.com  | PM     |
+----------+--------+----------+--------+
```

**tareas**
```
+-------+-------+----------+-----------+-------+------------+
| id    | título| desc.    | f_límite | estado| emp_id(FK) |
+-------+-------+----------+-----------+-------+------------+
| 1     | Auth  | JWT      | 12/31/24  | Pend. | 1          |
| 2     | Docs  | Update   | 12/25/24  | Proc. | 2          |
| 3     | Test  | NULL     | 12/20/24  | Pend. | NULL       |
+-------+-------+----------+-----------+-------+------------+
```

### Relaciones

- **1:N** (Empleado:Tareas)
- Integridad referencial: `FOREIGN KEY (empleado_id) REFERENCES empleados(id)`
- Acción en eliminar: `ON DELETE SET NULL` (las tareas quedan sin asignación)

## Validación en Capas

### Capa 1: OpenAPI (Controller)
```python
# Pydantic valida automáticamente
class EmpleadoCrear(BaseModel):
    nombre: str = Field(..., min_length=1)
    correo: EmailStr  # Valida formato email
    cargo: str = Field(..., min_length=1)
```

### Capa 2: Lógica de Negocio (Service)
```python
# Validar reglas de negocio
if self.empleado_repository.obtener_por_correo(correo) is not None:
    raise ValueError(f"Correo '{correo}' ya registrado")
```

### Capa 3: Integridad de Datos (Repository)
```python
# Validar en base de datos
try:
    cursor.execute("INSERT INTO empleados (correo) VALUES (?)", (correo,))
    # UNIQUE constraint en BD previene duplicados
except sqlite3.IntegrityError:
    raise ValueError("Correo duplicado")
```

## Manejo de Errores

### Estrategia de Respuestas HTTP

| Status | Scenario | Ejemplo |
|--------|----------|----------|
| 201 | Recurso creado | POST /empleados ✓ |
| 200 | Operación exitosa | GET /empleados ✓ |
| 400 | Datos inválidos | Nombre vacío |
| 409 | Conflicto (duplicado) | Correo ya registrado |
| 404 | Recurso no existe | Empleado no encontrado |
| 500 | Error servidor | Excepción no manejada |

### Flujo de Manejo

```python
try:
    empleado = service.registrar_empleado(...)
    return EmpleadoRespuesta(**empleado)  # 201
except ValueError as e:
    # Lógica de negocio fallida
    if "ya registrado" in str(e):
        raise HTTPException(status_code=409, detail=str(e))  # Conflict
    else:
        raise HTTPException(status_code=400, detail=str(e))  # Bad Request
except Exception as e:
    raise HTTPException(status_code=500, detail="Error interno")  # Error
```

## Testing

### Estrategia de Testing

```python
# Test del Servicio (sin BD real)
def test_registrar_empleado_duplicado():
    mock_repo = Mock(spec=IEmpleadoRepository)
    mock_repo.obtener_por_correo.return_value = {"id": 1}  # Ya existe
    
    service = EmpleadoService(mock_repo)
    
    with pytest.raises(ValueError, match="ya registrado"):
        service.registrar_empleado("Juan", "juan@e.com", "Dev")
```

**Beneficio de la arquitectura:** Mockear interfaz, NO implementación concreta.

## Escalabilidad Futura

### Mejoras Planeadas

1. **Autenticación & Autorización**
   - OAuth2 + JWT
   - Roles: Admin, Manager, Employee

2. **Base de Datos Avanzada**
   - Migrar a PostgreSQL
   - Paginación y filtrado
   - Índices para performance

3. **Caching**
   - Redis para datos frecuentes
   - Invalidación inteligente

4. **Async/Await**
   - Operaciones de BD no-bloqueantes
   - Mayor concurrencia

5. **Logging & Monitoreo**
   - Logs estructurados (JSON)
   - APM (Application Performance Monitoring)

6. **Testing Completo**
   - Unit tests (servicios)
   - Integration tests (BD)
   - End-to-end tests (APIs)

## Conclusión

Esta arquitectura proporciona una base sólida, mantenible y escalable para el Sistema de Gestión de Tareas, implementando principios de diseño de software de nivel empresarial.
