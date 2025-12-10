# CAMPUS360 Auth - Monorepo

Sistema de autenticación completo para CAMPUS360 con backend FastAPI y frontend React.

## 📁 Estructura del Proyecto

```
campus360-auth/
├── campus360-auth-backend/     # Backend FastAPI + Prisma
│   ├── app/                    # Código de la aplicación
│   ├── prisma/                 # Esquemas de base de datos
│   ├── .venv/                  # Entorno virtual Python
│   ├── .env                    # Variables de entorno
│   └── requirements.txt        # Dependencias Python
│
├── campus360-auth-frontend/    # Frontend React + Vite
│   ├── src/                    # Código fuente
│   ├── public/                 # Archivos estáticos
│   ├── package.json            # Dependencias Node
│   └── vite.config.js          # Configuración Vite
│
└── README.md                   # Este archivo
```

## 🚀 Inicio Rápido

### Backend (Puerto 8000)

```bash
cd campus360-auth-backend

# Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

# Instalar dependencias (si es necesario)
pip install -r requirements.txt

# Generar cliente Prisma
export PATH="$HOME/.local/bin:$PATH"
python -m prisma py generate

# Aplicar migraciones
python -m prisma db push

# Iniciar servidor
uvicorn app.main:app --reload
```

El backend estará disponible en: **http://localhost:8000**
- Documentación API: http://localhost:8000/docs
- Documentación alternativa: http://localhost:8000/redoc

### Frontend (Puerto 5173)

```bash
cd campus360-auth-frontend

# Instalar dependencias (primera vez)
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

## 🔧 Configuración

### Backend (.env)

Crea o edita `campus360-auth-backend/.env`:

```env
DATABASE_URL="postgresql://usuario:password@host:puerto/database"
SECRET_KEY="tu-clave-secreta-super-segura"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend

La configuración de la API está en `campus360-auth-frontend/src/api/api.js`:
- Por defecto apunta a `http://localhost:8000`
- Cambiar `API_URL` si el backend está en otro puerto

## 📝 Comandos Útiles

### Backend

```bash
# Regenerar cliente Prisma (después de cambiar schema)
python -m prisma py generate

# Ver logs de Prisma
python -m prisma studio

# Ejecutar tests
pytest
```

### Frontend

```bash
# Compilar para producción
npm run build

# Preview de producción
npm run preview

# Linter
npm run lint
```

## 🔐 Características

- ✅ Autenticación JWT
- ✅ Registro y login de usuarios
- ✅ Credencial digital con QR
- ✅ Escáner de QR con cámara
- ✅ Registro de accesos a ubicaciones
- ✅ Historial de accesos
- ✅ Panel de administración

## 🛠️ Tecnologías

**Backend:**
- FastAPI
- Prisma ORM
- PostgreSQL (Supabase)
- JWT Authentication
- QR Code Generation

**Frontend:**
- React
- Vite
- React Router
- HTML5 QR Code Scanner
- Tailwind CSS (si aplica)

## 📦 Despliegue

### Backend
- Configurar `DATABASE_URL` con la base de datos de producción
- Cambiar `SECRET_KEY` a una clave segura
- Desactivar `--reload` en producción

### Frontend
- Actualizar `API_URL` en `src/api/api.js` con la URL del backend en producción
- Ejecutar `npm run build`
- Servir la carpeta `dist/` con un servidor web

## 👥 Equipo

CAMPUS360 - PUCESM
