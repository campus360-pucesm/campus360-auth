# CAMPUS360 - Authentication Module API Documentation

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [URL Base](#url-base)
- [Autenticación](#autenticación)
- [Endpoints](#endpoints)
  - [Autenticación](#endpoints-de-autenticación)
  - [QR Access](#endpoints-de-qr-access)
  - [Administración de Usuarios](#endpoints-de-administración-de-usuarios)
  - [Administración - Dashboard](#endpoints-de-dashboard-administrativo)
  - [Health Check](#health-check)
- [Modelos de Datos](#modelos-de-datos)
- [Códigos de Error](#códigos-de-error)
- [Ejemplos de Integración](#ejemplos-de-integración)

---

## Descripción General

El módulo de autenticación CAMPUS360 es una API RESTful que proporciona:

- 🔐 **Autenticación JWT** - Sistema seguro de login con tokens
- 📱 **Control de Acceso QR** - Gestión de acceso mediante códigos QR
- 👥 **Gestión de Usuarios** - CRUD completo de usuarios (admin, teacher, student)
- 📊 **Dashboard Administrativo** - Estadísticas y monitoreo de accesos

---

## URL Base

### Producción
```
https://your-app-name.onrender.com
```

### Desarrollo
```
http://localhost:8000
```

### Documentación Interactiva
```
https://your-app-name.onrender.com/docs
```

---

## Autenticación

La API utiliza **JWT (JSON Web Tokens)** para autenticación.

### Flujo de Autenticación

1. **Login**: Enviar credenciales a `/auth/login`
2. **Recibir Token**: La API devuelve un `access_token`
3. **Usar Token**: Incluir el token en el header `Authorization` de las peticiones protegidas

### Header de Autenticación

```http
Authorization: Bearer <access_token>
```

### Ejemplo
```javascript
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};
```

---

## Endpoints

### Endpoints de Autenticación

#### 1. Login

Autenticar usuario y obtener token JWT.

**Endpoint:** `POST /auth/login`

**Autenticación:** No requerida

**Content-Type:** `application/x-www-form-urlencoded`

**Parámetros del Body:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| username | string | Sí | Email del usuario |
| password | string | Sí | Contraseña |

**Respuesta Exitosa (200):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Ejemplo con JavaScript:**

```javascript
const formData = new URLSearchParams();
formData.append('username', 'usuario@example.com');
formData.append('password', 'password123');

const response = await fetch('https://your-api.onrender.com/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: formData
});

const data = await response.json();
localStorage.setItem('token', data.access_token);
```

**Ejemplo con Python:**

```python
import requests

response = requests.post(
    'https://your-api.onrender.com/auth/login',
    data={
        'username': 'usuario@example.com',
        'password': 'password123'
    }
)

token = response.json()['access_token']
```

**Errores:**

- `401 Unauthorized` - Credenciales incorrectas

---

### Endpoints de QR Access

#### 2. Obtener Perfil de Usuario

Obtener información del usuario autenticado para generar QR de credencial.

**Endpoint:** `GET /qr/me`

**Autenticación:** Requerida (Bearer Token)

**Respuesta Exitosa (200):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "estudiante@pucesm.edu.ec",
  "full_name": "Juan Pérez",
  "role": "student",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Ejemplo con JavaScript:**

```javascript
const token = localStorage.getItem('token');

const response = await fetch('https://your-api.onrender.com/qr/me', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const userData = await response.json();
console.log(userData);
```

**Errores:**

- `401 Unauthorized` - Token inválido o expirado

---

#### 3. Registrar Acceso (Escaneo QR)

Registrar acceso a una ubicación mediante escaneo de QR.

**Endpoint:** `POST /qr/scan`

**Autenticación:** Requerida (Bearer Token)

**Body (JSON):**

```json
{
  "location_code": "LAB-101"
}
```

**Parámetros:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| location_code | string | Sí | Código de ubicación del QR escaneado |

**Respuesta Exitosa (200):**

```json
{
  "message": "Access recorded successfully",
  "location_code": "LAB-101",
  "timestamp": "2024-01-15T14:30:00Z",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "estudiante@pucesm.edu.ec",
    "full_name": "Juan Pérez",
    "role": "student",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Ejemplo con JavaScript:**

```javascript
const token = localStorage.getItem('token');

const response = await fetch('https://your-api.onrender.com/qr/scan', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    location_code: 'LAB-101'
  })
});

const result = await response.json();
console.log(result.message);
```

**Errores:**

- `401 Unauthorized` - Token inválido o expirado

---

#### 4. Historial de Accesos

Obtener historial de accesos del usuario autenticado.

**Endpoint:** `GET /qr/history`

**Autenticación:** Requerida (Bearer Token)

**Query Parameters:**

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| limit | integer | No | 10 | Número máximo de registros (max: 100) |

**Respuesta Exitosa (200):**

```json
[
  {
    "id": 1,
    "location_code": "LAB-101",
    "timestamp": "2024-01-15T14:30:00Z"
  },
  {
    "id": 2,
    "location_code": "AULA-302",
    "timestamp": "2024-01-15T10:15:00Z"
  }
]
```

**Ejemplo con JavaScript:**

```javascript
const token = localStorage.getItem('token');

const response = await fetch('https://your-api.onrender.com/qr/history?limit=20', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const history = await response.json();
console.log(history);
```

---

### Endpoints de Administración de Usuarios

> **⚠️ Nota:** Todos estos endpoints requieren rol de **admin**

#### 5. Crear Usuario

Crear un nuevo usuario (admin, teacher o student).

**Endpoint:** `POST /admin/users`

**Autenticación:** Requerida (Bearer Token - Admin)

**Body (JSON):**

```json
{
  "email": "nuevo@pucesm.edu.ec",
  "password": "password123",
  "full_name": "María García",
  "role": "student"
}
```

**Parámetros:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| email | string | Sí | Email único del usuario |
| password | string | Sí | Contraseña (mínimo 6 caracteres) |
| full_name | string | Sí | Nombre completo |
| role | string | Sí | Rol: "admin", "teacher" o "student" |

**Respuesta Exitosa (201):**

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "email": "nuevo@pucesm.edu.ec",
  "full_name": "María García",
  "role": "student",
  "created_at": "2024-01-15T15:00:00Z"
}
```

**Ejemplo con JavaScript:**

```javascript
const token = localStorage.getItem('token');

const response = await fetch('https://your-api.onrender.com/admin/users', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'nuevo@pucesm.edu.ec',
    password: 'password123',
    full_name: 'María García',
    role: 'student'
  })
});

const newUser = await response.json();
```

**Errores:**

- `400 Bad Request` - Email ya registrado o rol inválido
- `403 Forbidden` - Usuario no es admin

---

#### 6. Listar Usuarios

Obtener lista de todos los usuarios con filtros opcionales.

**Endpoint:** `GET /admin/users`

**Autenticación:** Requerida (Bearer Token - Admin)

**Query Parameters:**

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| skip | integer | No | 0 | Registros a omitir (paginación) |
| limit | integer | No | 100 | Número máximo de registros |
| role | string | No | - | Filtrar por rol: "admin", "teacher", "student" |

**Respuesta Exitosa (200):**

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "admin@pucesm.edu.ec",
    "full_name": "Administrador",
    "role": "admin",
    "created_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "email": "estudiante@pucesm.edu.ec",
    "full_name": "Juan Pérez",
    "role": "student",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

**Ejemplo con JavaScript:**

```javascript
const token = localStorage.getItem('token');

// Obtener todos los estudiantes
const response = await fetch('https://your-api.onrender.com/admin/users?role=student&limit=50', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const students = await response.json();
```

**Errores:**

- `403 Forbidden` - Usuario no es admin

---

#### 7. Obtener Usuario por ID

Obtener detalles de un usuario específico.

**Endpoint:** `GET /admin/users/{user_id}`

**Autenticación:** Requerida (Bearer Token - Admin)

**Path Parameters:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| user_id | string (UUID) | ID del usuario |

**Respuesta Exitosa (200):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "estudiante@pucesm.edu.ec",
  "full_name": "Juan Pérez",
  "role": "student",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Ejemplo con JavaScript:**

```javascript
const token = localStorage.getItem('token');
const userId = '550e8400-e29b-41d4-a716-446655440000';

const response = await fetch(`https://your-api.onrender.com/admin/users/${userId}`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const user = await response.json();
```

**Errores:**

- `403 Forbidden` - Usuario no es admin
- `404 Not Found` - Usuario no encontrado

---

#### 8. Actualizar Usuario

Actualizar información de un usuario.

**Endpoint:** `PUT /admin/users/{user_id}`

**Autenticación:** Requerida (Bearer Token - Admin)

**Path Parameters:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| user_id | string (UUID) | ID del usuario |

**Body (JSON):** (Todos los campos son opcionales)

```json
{
  "email": "nuevo_email@pucesm.edu.ec",
  "full_name": "Juan Carlos Pérez",
  "role": "teacher",
  "password": "nueva_password"
}
```

**Respuesta Exitosa (200):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "nuevo_email@pucesm.edu.ec",
  "full_name": "Juan Carlos Pérez",
  "role": "teacher",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Ejemplo con JavaScript:**

```javascript
const token = localStorage.getItem('token');
const userId = '550e8400-e29b-41d4-a716-446655440000';

const response = await fetch(`https://your-api.onrender.com/admin/users/${userId}`, {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    role: 'teacher',
    full_name: 'Juan Carlos Pérez'
  })
});

const updatedUser = await response.json();
```

**Errores:**

- `400 Bad Request` - Email ya en uso o rol inválido
- `403 Forbidden` - Usuario no es admin
- `404 Not Found` - Usuario no encontrado

---

#### 9. Eliminar Usuario

Eliminar un usuario del sistema.

**Endpoint:** `DELETE /admin/users/{user_id}`

**Autenticación:** Requerida (Bearer Token - Admin)

**Path Parameters:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| user_id | string (UUID) | ID del usuario |

**Respuesta Exitosa (204):** Sin contenido

**Ejemplo con JavaScript:**

```javascript
const token = localStorage.getItem('token');
const userId = '550e8400-e29b-41d4-a716-446655440000';

const response = await fetch(`https://your-api.onrender.com/admin/users/${userId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

if (response.status === 204) {
  console.log('Usuario eliminado exitosamente');
}
```

**Errores:**

- `400 Bad Request` - No se puede eliminar la propia cuenta
- `403 Forbidden` - Usuario no es admin
- `404 Not Found` - Usuario no encontrado

---

### Endpoints de Dashboard Administrativo

#### 10. Estadísticas del Sistema

Obtener estadísticas generales del sistema.

**Endpoint:** `GET /admin/stats`

**Autenticación:** Requerida (Bearer Token - Admin)

**Respuesta Exitosa (200):**

```json
{
  "total_users": 150,
  "total_students": 120,
  "total_teachers": 25,
  "total_admins": 5,
  "total_access_logs": 1250,
  "access_today": 45
}
```

**Ejemplo con JavaScript:**

```javascript
const token = localStorage.getItem('token');

const response = await fetch('https://your-api.onrender.com/admin/stats', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const stats = await response.json();
console.log(`Total usuarios: ${stats.total_users}`);
```

---

#### 11. Accesos Recientes

Obtener los accesos más recientes del sistema.

**Endpoint:** `GET /admin/recent-access`

**Autenticación:** Requerida (Bearer Token - Admin)

**Query Parameters:**

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| limit | integer | No | 10 | Número de registros (max: 100) |

**Respuesta Exitosa (200):**

```json
[
  {
    "id": 1250,
    "location_code": "LAB-101",
    "timestamp": "2024-01-15T14:30:00Z",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "estudiante@pucesm.edu.ec",
      "full_name": "Juan Pérez",
      "role": "student"
    }
  }
]
```

**Ejemplo con JavaScript:**

```javascript
const token = localStorage.getItem('token');

const response = await fetch('https://your-api.onrender.com/admin/recent-access?limit=20', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const recentAccess = await response.json();
```

---

### Health Check

#### 12. Verificar Estado de la API

**Endpoint:** `GET /health`

**Autenticación:** No requerida

**Respuesta Exitosa (200):**

```json
{
  "status": "healthy",
  "database": "connected"
}
```

#### 13. Root Endpoint

**Endpoint:** `GET /`

**Autenticación:** No requerida

**Respuesta Exitosa (200):**

```json
{
  "message": "CAMPUS360 Authentication Module",
  "status": "running",
  "version": "1.0.0"
}
```

---

## Modelos de Datos

### User

```typescript
{
  id: string;              // UUID
  email: string;           // Email único
  full_name: string;       // Nombre completo
  role: string;            // "admin" | "teacher" | "student"
  created_at: string;      // ISO 8601 timestamp
}
```

### AccessLog

```typescript
{
  id: number;              // ID autoincremental
  location_code: string;   // Código de ubicación
  timestamp: string;       // ISO 8601 timestamp
}
```

### Token

```typescript
{
  access_token: string;    // JWT token
  token_type: string;      // "bearer"
}
```

---

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | OK - Petición exitosa |
| 201 | Created - Recurso creado exitosamente |
| 204 | No Content - Operación exitosa sin contenido |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Autenticación requerida o inválida |
| 403 | Forbidden - Sin permisos para esta operación |
| 404 | Not Found - Recurso no encontrado |
| 422 | Unprocessable Entity - Error de validación |
| 500 | Internal Server Error - Error del servidor |

### Formato de Error

```json
{
  "detail": "Descripción del error"
}
```

---

## Ejemplos de Integración

### Ejemplo Completo: Login y Obtener Perfil

```javascript
// 1. Login
async function login(email, password) {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await fetch('https://your-api.onrender.com/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }

  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data.access_token;
}

// 2. Obtener perfil
async function getProfile() {
  const token = localStorage.getItem('token');
  
  const response = await fetch('https://your-api.onrender.com/qr/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error('Failed to get profile');
  }

  return await response.json();
}

// Uso
try {
  await login('usuario@pucesm.edu.ec', 'password123');
  const profile = await getProfile();
  console.log('Usuario:', profile.full_name);
} catch (error) {
  console.error('Error:', error.message);
}
```

### Ejemplo: Crear Usuario (Admin)

```javascript
async function createUser(userData) {
  const token = localStorage.getItem('token');
  
  const response = await fetch('https://your-api.onrender.com/admin/users', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(userData)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return await response.json();
}

// Uso
try {
  const newUser = await createUser({
    email: 'nuevo@pucesm.edu.ec',
    password: 'password123',
    full_name: 'María García',
    role: 'student'
  });
  console.log('Usuario creado:', newUser.id);
} catch (error) {
  console.error('Error:', error.message);
}
```

### Ejemplo con Python (requests)

```python
import requests

class Campus360API:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
    
    def login(self, email, password):
        response = requests.post(
            f'{self.base_url}/auth/login',
            data={'username': email, 'password': password}
        )
        response.raise_for_status()
        self.token = response.json()['access_token']
        return self.token
    
    def get_profile(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f'{self.base_url}/qr/me', headers=headers)
        response.raise_for_status()
        return response.json()
    
    def create_user(self, user_data):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(
            f'{self.base_url}/admin/users',
            headers=headers,
            json=user_data
        )
        response.raise_for_status()
        return response.json()

# Uso
api = Campus360API('https://your-api.onrender.com')
api.login('admin@pucesm.edu.ec', 'password')
profile = api.get_profile()
print(f'Usuario: {profile["full_name"]}')
```

---

## Notas Importantes

1. **Tokens JWT**: Los tokens tienen una expiración de 30 minutos por defecto
2. **CORS**: La API acepta peticiones desde cualquier origen en desarrollo. En producción, configurar `FRONTEND_URL`
3. **Rate Limiting**: Considerar implementar rate limiting en producción
4. **HTTPS**: Siempre usar HTTPS en producción
5. **Validación**: Todos los endpoints validan los datos de entrada

---

## Soporte

Para más información, consultar la documentación interactiva en `/docs` cuando el servidor esté corriendo.

**Documentación Swagger UI:** `https://your-api.onrender.com/docs`
**Documentación ReDoc:** `https://your-api.onrender.com/redoc`
