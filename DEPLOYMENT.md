# 🚀 Guía de Despliegue - CAMPUS360 Auth Module

Esta guía te llevará paso a paso por el proceso de despliegue del módulo de autenticación CAMPUS360 en Render (backend) y Vercel (frontend).

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Parte 1: Desplegar Backend en Render](#parte-1-desplegar-backend-en-render)
- [Parte 2: Desplegar Frontend en Vercel](#parte-2-desplegar-frontend-en-vercel)
- [Parte 3: Configuración Post-Despliegue](#parte-3-configuración-post-despliegue)
- [Verificación](#verificación)
- [Solución de Problemas](#solución-de-problemas)

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

- ✅ Cuenta en [Render](https://render.com) (gratis)
- ✅ Cuenta en [Vercel](https://vercel.com) (gratis)
- ✅ Cuenta en [Supabase](https://supabase.com) con base de datos PostgreSQL configurada
- ✅ Repositorio Git con el código (GitHub, GitLab, o Bitbucket)
- ✅ Git instalado localmente

---

## Parte 1: Desplegar Backend en Render

### Paso 1.1: Preparar el Repositorio

1. **Asegúrate de que todos los archivos estén en el repositorio:**

```bash
cd campus360-auth/campus360-auth-backend
git add .
git commit -m "Preparar backend para despliegue en Render"
git push origin main
```

2. **Verifica que estos archivos existan:**
   - ✅ `render.yaml`
   - ✅ `build.sh`
   - ✅ `requirements.txt`
   - ✅ `prisma/schema.prisma`

### Paso 1.2: Crear Servicio en Render

1. **Ir a [Render Dashboard](https://dashboard.render.com)**

2. **Crear nuevo Web Service:**
   - Click en "New +" → "Web Service"

3. **Conectar repositorio:**
   - Selecciona tu repositorio Git
   - Si es la primera vez, autoriza a Render para acceder a tu cuenta de GitHub/GitLab

4. **Configurar el servicio:**

   | Campo | Valor |
   |-------|-------|
   | **Name** | `campus360-auth-api` (o el nombre que prefieras) |
   | **Region** | Selecciona la más cercana (ej: Oregon, USA) |
   | **Branch** | `main` |
   | **Root Directory** | `campus360-auth-backend` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `./build.sh` |
   | **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | **Plan** | `Free` |

### Paso 1.3: Configurar Variables de Entorno

En la sección "Environment Variables", agrega las siguientes variables:

#### Variables Requeridas:

1. **DATABASE_URL**
   ```
   Valor: Tu URL de Supabase PostgreSQL
   Ejemplo: postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```
   
   > 💡 **Cómo obtenerla:**
   > - Ve a tu proyecto en Supabase
   > - Settings → Database → Connection String
   > - Copia "Session Pooler" (puerto 6543)
   > - Reemplaza `[YOUR-PASSWORD]` con tu contraseña

2. **SECRET_KEY**
   ```
   Valor: Genera una clave secreta
   ```
   
   > 💡 **Generar clave segura:**
   > ```bash
   > openssl rand -hex 32
   > ```
   > O usa el generador automático de Render

3. **ALGORITHM**
   ```
   Valor: HS256
   ```

4. **ACCESS_TOKEN_EXPIRE_MINUTES**
   ```
   Valor: 30
   ```

5. **PYTHON_VERSION**
   ```
   Valor: 3.11.0
   ```

### Paso 1.4: Desplegar

1. Click en **"Create Web Service"**

2. Render comenzará a:
   - ✅ Clonar tu repositorio
   - ✅ Ejecutar `build.sh`
   - ✅ Instalar dependencias
   - ✅ Generar cliente Prisma
   - ✅ Crear tablas en la base de datos
   - ✅ Iniciar el servidor

3. **Espera a que el despliegue termine** (5-10 minutos la primera vez)

4. **Copia la URL de tu API:**
   ```
   https://campus360-auth-api.onrender.com
   ```
   (Será algo similar, con tu nombre de servicio)

### Paso 1.5: Verificar Backend

Abre en tu navegador:

```
https://tu-app.onrender.com/docs
```

Deberías ver la documentación interactiva de Swagger UI.

---

## Parte 2: Desplegar Frontend en Vercel

### Paso 2.1: Preparar el Repositorio

1. **Asegúrate de que los archivos estén en el repositorio:**

```bash
cd campus360-auth/campus360-auth-frontend
git add .
git commit -m "Preparar frontend para despliegue en Vercel"
git push origin main
```

2. **Verifica que estos archivos existan:**
   - ✅ `vercel.json`
   - ✅ `package.json`
   - ✅ `src/config/api.js`

### Paso 2.2: Crear Proyecto en Vercel

1. **Ir a [Vercel Dashboard](https://vercel.com/dashboard)**

2. **Importar proyecto:**
   - Click en "Add New..." → "Project"
   - Selecciona tu repositorio Git
   - Si es la primera vez, autoriza a Vercel

3. **Configurar el proyecto:**

   | Campo | Valor |
   |-------|-------|
   | **Project Name** | `campus360-auth` (o el nombre que prefieras) |
   | **Framework Preset** | `Vite` |
   | **Root Directory** | `campus360-auth-frontend` |
   | **Build Command** | `npm run build` |
   | **Output Directory** | `dist` |

### Paso 2.3: Configurar Variables de Entorno

En la sección "Environment Variables":

1. **VITE_API_URL**
   ```
   Valor: https://tu-app.onrender.com
   ```
   (La URL que copiaste del backend en Render)

   > ⚠️ **Importante:** NO incluyas `/` al final de la URL

### Paso 2.4: Desplegar

1. Click en **"Deploy"**

2. Vercel comenzará a:
   - ✅ Clonar tu repositorio
   - ✅ Instalar dependencias (`npm install`)
   - ✅ Construir el proyecto (`npm run build`)
   - ✅ Desplegar a CDN global

3. **Espera a que el despliegue termine** (2-5 minutos)

4. **Copia la URL de tu frontend:**
   ```
   https://campus360-auth.vercel.app
   ```
   (Será algo similar, con tu nombre de proyecto)

---

## Parte 3: Configuración Post-Despliegue

### Paso 3.1: Actualizar CORS en Backend

1. **Ir a Render Dashboard** → Tu servicio backend

2. **Environment Variables** → Agregar nueva variable:

   ```
   FRONTEND_URL = https://campus360-auth.vercel.app
   ```
   (Tu URL de Vercel)

3. **Guardar cambios** - Render redesplegará automáticamente

### Paso 3.2: Crear Usuario Administrador Inicial

Tienes dos opciones:

#### Opción A: Usar Supabase SQL Editor

1. Ve a tu proyecto en Supabase
2. SQL Editor → New Query
3. Ejecuta este SQL (reemplaza los valores):

```sql
INSERT INTO users (id, email, password_hash, full_name, role, created_at)
VALUES (
  gen_random_uuid(),
  'admin@pucesm.edu.ec',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPGxNKZXSu', -- password: admin123
  'Administrador',
  'admin',
  NOW()
);
```

> ⚠️ **Nota:** El hash corresponde a la contraseña `admin123`. Cámbiala después del primer login.

#### Opción B: Generar hash de contraseña

Si quieres usar tu propia contraseña:

```python
# En tu terminal local con Python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = pwd_context.hash("tu_password_aqui")
print(password_hash)
```

Luego usa ese hash en el SQL de arriba.

---

## Verificación

### ✅ Checklist de Verificación

1. **Backend (API):**
   - [ ] La URL `/docs` muestra la documentación Swagger
   - [ ] La URL `/health` devuelve `{"status": "healthy"}`
   - [ ] Puedes hacer login desde Postman o similar

2. **Frontend:**
   - [ ] La página de login se carga correctamente
   - [ ] Puedes hacer login con el usuario admin
   - [ ] El dashboard se muestra después del login
   - [ ] No hay errores de CORS en la consola del navegador

3. **Integración:**
   - [ ] El frontend puede comunicarse con el backend
   - [ ] Los tokens JWT funcionan correctamente
   - [ ] Las peticiones autenticadas funcionan

### Prueba Manual Completa

1. **Abre tu frontend:** `https://tu-app.vercel.app`

2. **Haz login** con el usuario admin creado

3. **Verifica el panel de administración:**
   - Estadísticas se cargan
   - Puedes crear un nuevo usuario
   - Puedes ver la lista de usuarios

4. **Prueba QR Access:**
   - Ve a la sección de perfil
   - Verifica que se muestre tu información
   - Prueba escanear un código QR (si tienes la funcionalidad)

---

## Solución de Problemas

### ❌ Error: "Build failed" en Render

**Problema:** El script `build.sh` falla

**Solución:**
1. Verifica que `build.sh` tenga permisos de ejecución:
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Fix build.sh permissions"
   git push
   ```

2. Revisa los logs en Render para ver el error específico

### ❌ Error: "Database connection failed"

**Problema:** No puede conectar a Supabase

**Solución:**
1. Verifica que `DATABASE_URL` esté correctamente configurada
2. Asegúrate de usar el "Session Pooler" (puerto 6543), no el "Direct Connection"
3. Verifica que la contraseña no tenga caracteres especiales sin escapar

### ❌ Error: CORS en el navegador

**Problema:** `Access-Control-Allow-Origin` error

**Solución:**
1. Verifica que `FRONTEND_URL` esté configurada en Render
2. Asegúrate de que la URL sea exacta (sin `/` al final)
3. Espera a que Render redesplegue después de cambiar variables

### ❌ Error: "Module not found" en Vercel

**Problema:** Falta alguna dependencia

**Solución:**
1. Verifica que `package.json` tenga todas las dependencias
2. En Vercel, ve a Settings → General → Node.js Version
3. Asegúrate de usar Node.js 18.x o superior

### ❌ Error: 404 en rutas del frontend

**Problema:** Las rutas de React Router no funcionan

**Solución:**
- Verifica que `vercel.json` exista y tenga la configuración de rewrites correcta

### ❌ Backend en Render se "duerme"

**Problema:** El plan gratuito de Render pone a dormir servicios inactivos

**Solución:**
- Es normal en el plan gratuito
- La primera petición después de inactividad tardará ~30 segundos
- Para evitarlo, considera:
  - Upgrade a plan pagado ($7/mes)
  - Usar un servicio de "ping" como UptimeRobot (gratis)

---

## Mantenimiento

### Actualizar el Backend

```bash
# Hacer cambios en el código
git add .
git commit -m "Descripción de cambios"
git push origin main

# Render redesplegará automáticamente
```

### Actualizar el Frontend

```bash
# Hacer cambios en el código
git add .
git commit -m "Descripción de cambios"
git push origin main

# Vercel redesplegará automáticamente
```

### Ver Logs

**Render:**
- Dashboard → Tu servicio → Logs

**Vercel:**
- Dashboard → Tu proyecto → Deployments → Click en deployment → View Function Logs

---

## URLs de Referencia

- **Documentación de Render:** https://render.com/docs
- **Documentación de Vercel:** https://vercel.com/docs
- **Documentación de Supabase:** https://supabase.com/docs
- **Documentación de FastAPI:** https://fastapi.tiangolo.com
- **Documentación de Prisma:** https://www.prisma.io/docs

---

## Próximos Pasos

Una vez desplegado, considera:

1. **Configurar dominio personalizado** en Vercel
2. **Configurar alertas** de monitoreo
3. **Implementar backups** de la base de datos
4. **Agregar analytics** (Google Analytics, Plausible, etc.)
5. **Configurar CI/CD** para tests automáticos

---

## Soporte

Si tienes problemas durante el despliegue:

1. Revisa los logs en Render/Vercel
2. Consulta la sección de "Solución de Problemas" arriba
3. Revisa la documentación de la API en `/docs`

¡Buena suerte con tu despliegue! 🚀
