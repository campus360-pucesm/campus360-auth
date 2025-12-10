# 🎓 CAMPUS360 - Authentication Module

Sistema de autenticación inteligente con control de acceso basado en códigos QR para instituciones educativas.

---

## 📋 Descripción

El módulo de autenticación CAMPUS360 proporciona una API RESTful completa para:

- 🔐 **Autenticación JWT** - Sistema seguro de login con tokens
- 📱 **Control de Acceso QR** - Gestión de acceso mediante códigos QR
- 👥 **Gestión de Usuarios** - CRUD completo de usuarios (admin, teacher, student)
- 📊 **Dashboard Administrativo** - Estadísticas y monitoreo de accesos

Este módulo está diseñado para ser consumido como API por otros módulos del ecosistema CAMPUS360.

---

## 🚀 Inicio Rápido

### Desarrollo Local

#### Backend
```bash
cd campus360-auth-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edita .env con tus credenciales de Supabase
python -m prisma generate
python -m prisma db push
uvicorn app.main:app --reload
```

Visita: http://localhost:8000/docs

#### Frontend
```bash
cd campus360-auth-frontend
npm install
cp .env.example .env
# Edita .env si es necesario
npm run dev
```

Visita: http://localhost:5173

---

## 📚 Documentación

### 📖 API Documentation
**[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Documentación completa de la API

Incluye:
- 13 endpoints documentados
- Ejemplos en JavaScript y Python
- Esquemas de request/response
- Códigos de error
- Guías de integración

### 🚀 Deployment Guide
**[DEPLOYMENT.md](./DEPLOYMENT.md)** - Guía de despliegue paso a paso

Cubre:
- Despliegue en Render (Backend)
- Despliegue en Vercel (Frontend)
- Configuración de variables de entorno
- Solución de problemas
- Verificación post-despliegue

### 📝 Backend README
**[campus360-auth-backend/README.md](./campus360-auth-backend/README.md)** - Documentación del backend

### 🎨 Frontend README
**[campus360-auth-frontend/README.md](./campus360-auth-frontend/README.md)** - Documentación del frontend

---

## 🏗️ Arquitectura

```
campus360-auth/
├── campus360-auth-backend/     # FastAPI + Prisma + Supabase
│   ├── app/
│   │   ├── routers/           # Endpoints de la API
│   │   ├── schemas/           # Modelos Pydantic
│   │   ├── utils/             # Utilidades (JWT, auth)
│   │   └── main.py            # Aplicación FastAPI
│   ├── prisma/
│   │   └── schema.prisma      # Esquema de base de datos
│   ├── render.yaml            # Configuración Render
│   ├── build.sh               # Script de build
│   └── requirements.txt       # Dependencias Python
│
├── campus360-auth-frontend/    # React + Vite
│   ├── src/
│   │   ├── pages/             # Páginas de la app
│   │   ├── components/        # Componentes React
│   │   ├── config/            # Configuración API
│   │   └── context/           # Context API
│   ├── vercel.json            # Configuración Vercel
│   └── package.json           # Dependencias Node
│
├── API_DOCUMENTATION.md        # 📖 Documentación API
└── DEPLOYMENT.md               # 🚀 Guía de despliegue
```

---

## 🔌 Endpoints Principales

### Autenticación
- `POST /auth/login` - Login y obtener JWT token

### QR Access
- `GET /qr/me` - Obtener perfil de usuario
- `POST /qr/scan` - Registrar acceso a ubicación
- `GET /qr/history` - Historial de accesos

### Admin - Gestión de Usuarios
- `POST /admin/users` - Crear usuario
- `GET /admin/users` - Listar usuarios
- `GET /admin/users/{id}` - Obtener usuario
- `PUT /admin/users/{id}` - Actualizar usuario
- `DELETE /admin/users/{id}` - Eliminar usuario

### Admin - Dashboard
- `GET /admin/stats` - Estadísticas del sistema
- `GET /admin/recent-access` - Accesos recientes

Ver documentación completa en [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno de Python
- **Prisma** - ORM type-safe
- **Supabase** - Base de datos PostgreSQL
- **JWT** - Autenticación segura
- **Bcrypt** - Hash de contraseñas

### Frontend
- **React** - Biblioteca UI
- **Vite** - Build tool
- **React Router** - Enrutamiento
- **Context API** - Gestión de estado

### Deployment
- **Render** - Backend API (Plan gratuito)
- **Vercel** - Frontend (Plan gratuito)

---

## 🔐 Seguridad

- ✅ Hash de contraseñas con Bcrypt
- ✅ Autenticación JWT
- ✅ OAuth2 password flow
- ✅ Validación de email único
- ✅ Endpoints protegidos con dependency injection
- ✅ CORS configurable por entorno
- ✅ Security headers en producción

---

## 🌐 Despliegue en Producción

### Backend (Render)

1. Conecta tu repositorio Git a Render
2. Configura las variables de entorno:
   - `DATABASE_URL` - URL de Supabase
   - `SECRET_KEY` - Clave secreta JWT
   - `FRONTEND_URL` - URL del frontend
3. Render ejecutará automáticamente `build.sh`
4. Tu API estará disponible en `https://tu-app.onrender.com`

### Frontend (Vercel)

1. Importa tu proyecto en Vercel
2. Configura la variable de entorno:
   - `VITE_API_URL` - URL de tu API en Render
3. Vercel construirá y desplegará automáticamente
4. Tu frontend estará disponible en `https://tu-app.vercel.app`

**Ver guía completa:** [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 📊 Modelos de Datos

### User
```typescript
{
  id: string;              // UUID
  email: string;           // Email único
  full_name: string;       // Nombre completo
  role: string;            // "admin" | "teacher" | "student"
  created_at: string;      // Timestamp
}
```

### AccessLog
```typescript
{
  id: number;              // ID autoincremental
  user_id: string;         // UUID del usuario
  location_code: string;   // Código de ubicación
  timestamp: string;       // Timestamp
}
```

---

## 🔄 Integración con Otros Módulos

Este módulo está diseñado para ser consumido como API. Ejemplo de integración:

```javascript
// 1. Login
const response = await fetch('https://tu-api.onrender.com/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    username: 'usuario@example.com',
    password: 'password123'
  })
});

const { access_token } = await response.json();

// 2. Usar token en peticiones
const profile = await fetch('https://tu-api.onrender.com/qr/me', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
```

Ver más ejemplos en [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## 🧪 Testing

### Backend
```bash
cd campus360-auth-backend
pytest
```

### Frontend
```bash
cd campus360-auth-frontend
npm test
```

---

## 📝 Variables de Entorno

### Backend (.env)
```env
DATABASE_URL="postgresql://..."
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL="https://your-frontend.vercel.app"
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es parte del ecosistema CAMPUS360.

---

## 📞 Soporte

- **Documentación API:** [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Guía de Despliegue:** [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Swagger UI:** `https://tu-api.onrender.com/docs`
- **ReDoc:** `https://tu-api.onrender.com/redoc`

---

## 🎯 Roadmap

- [ ] Implementar refresh tokens
- [ ] Agregar rate limiting
- [ ] Implementar 2FA
- [ ] Agregar logs de auditoría
- [ ] Implementar notificaciones por email
- [ ] Agregar exportación de reportes
- [ ] Implementar búsqueda avanzada de usuarios

---

**Desarrollado para CAMPUS360** 🎓
