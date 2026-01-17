# Solución: Error "Invalid Segments" en JWT

## 🔍 Diagnóstico del Problema

El error **"Invalid segments"** ocurre cuando el token JWT está mal formado o corrupto. Este es un problema común que puede tener varias causas.

## ✅ Soluciones Implementadas

### 1. Mejor Manejo de Errores en el API Gateway

He mejorado el código del API Gateway para dar mensajes de error más específicos:

**Archivo:** `campus360-api-gateway/app/dependencies/auth_verifier.py`

Ahora el sistema detecta y reporta:
- ✅ Tokens expirados
- ✅ Tokens con formato inválido
- ✅ Tokens corruptos o incompletos
- ✅ Problemas con los claims del token

### 2. Limpieza Automática de Tokens

He agregado `.trim()` en el frontend para eliminar espacios en blanco que pueden corromper el token:

**Archivos modificados:**
- `campus360-web-app/src/contexts/AuthContext.jsx` - Al guardar el token
- `campus360-web-app/src/api/gateway.js` - Al enviar el token

## 🛠️ Pasos para Tu Compañero

### Paso 1: Actualizar el Código

```bash
# Hacer pull de los últimos cambios
git pull origin main

# Si el API Gateway está corriendo, reiniciarlo
# Ctrl+C para detener, luego:
cd campus360-api-gateway
uvicorn app.main:app --reload --port 8000
```

### Paso 2: Limpiar el Navegador

**IMPORTANTE:** Pídele que limpie el localStorage del navegador:

1. Abrir DevTools (F12)
2. Ir a la pestaña **Application** (o **Almacenamiento**)
3. En el menú izquierdo: **Local Storage** → `http://localhost:5173`
4. Click derecho → **Clear** (o eliminar las claves `token` y `user`)
5. Refrescar la página (F5)

### Paso 3: Verificar SECRET_KEY

Asegurarse de que el SECRET_KEY sea idéntico en ambos servicios:

```bash
# Backend de Autenticación
cat campus360-auth/campus360-auth-backend/.env | grep SECRET_KEY

# API Gateway
cat campus360-api-gateway/.env | grep SECRET_KEY
```

**Deben ser EXACTAMENTE iguales:**
```
SECRET_KEY=campus360-super-secret-key-change-in-production
```

Si no tiene el archivo `.env` en el API Gateway:
```bash
cd campus360-api-gateway
cp .env.example .env
```

### Paso 4: Reiniciar Todo

```bash
# Terminal 1 - Backend de Autenticación
cd campus360-auth/campus360-auth-backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8003

# Terminal 2 - API Gateway
cd campus360-api-gateway
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 3 - Frontend
cd campus360-web-app
npm run dev
```

### Paso 5: Probar Login

1. Ir a http://localhost:5173
2. Intentar login
3. **Revisar la consola del navegador** (F12 → Console)
4. **Revisar la pestaña Network** para ver el error exacto

## 🐛 Debugging Adicional

Si el error persiste, pídele que haga esto:

### Ver el Token en el Navegador

```javascript
// En la consola del navegador (F12 → Console)
console.log('Token:', localStorage.getItem('token'));
console.log('Token length:', localStorage.getItem('token')?.length);
```

**Verificar:**
- ✅ El token debe tener 3 partes separadas por puntos: `xxxxx.yyyyy.zzzzz`
- ✅ No debe tener espacios al inicio o final
- ✅ No debe estar `undefined` o `null`

### Ver el Error Completo

Con los cambios que hice, ahora el error será más específico. Pídele que:

1. Abra DevTools (F12)
2. Vaya a la pestaña **Network**
3. Intente hacer login
4. Click en la petición fallida
5. Vaya a la pestaña **Response**
6. **Copie el mensaje de error completo**

Ahora verá mensajes como:
- `"Token has expired"` → El token expiró
- `"Invalid token format. Token may be corrupted or incomplete."` → Token corrupto
- `"Invalid token claims"` → Problema con los datos del token

## 🔑 Causas Comunes del Error "Invalid Segments"

### 1. SECRET_KEY Diferente ❌
**Síntoma:** Token se genera pero no se puede validar

**Solución:**
```bash
# Verificar que sean iguales
grep SECRET_KEY campus360-auth/campus360-auth-backend/.env
grep SECRET_KEY campus360-api-gateway/.env
```

### 2. Token con Espacios en Blanco ❌
**Síntoma:** Error "Not enough segments" o "Invalid header"

**Solución:** Ya implementada con `.trim()` en el código

### 3. Token Corrupto en localStorage ❌
**Síntoma:** Token se ve raro o tiene caracteres extraños

**Solución:** Limpiar localStorage (ver Paso 2)

### 4. Versiones Diferentes de `python-jose` ❌
**Síntoma:** Token funciona en una máquina pero no en otra

**Solución:**
```bash
# En ambos servicios (auth backend y API gateway)
pip install --upgrade python-jose[cryptography]
```

### 5. Token No Se Está Enviando Correctamente ❌
**Síntoma:** Error en el API Gateway al recibir la petición

**Verificar en Network tab:**
```
Headers:
  Authorization: Bearer eyJhbGc...
```

Debe tener `Bearer` + espacio + token (sin espacios extra)

## 📋 Checklist de Verificación

Pídele a tu compañero que verifique:

- [ ] `git pull` ejecutado
- [ ] Archivo `.env` existe en `campus360-api-gateway/`
- [ ] SECRET_KEY es idéntico en ambos `.env`
- [ ] localStorage limpiado en el navegador
- [ ] Todos los servicios reiniciados
- [ ] Backend de Auth corriendo en puerto 8003
- [ ] API Gateway corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 5173
- [ ] No hay errores en la consola del backend
- [ ] DevTools abierto para ver errores específicos

## 🆘 Si Nada Funciona

Si después de todo esto sigue fallando, pídele que te envíe:

1. **Screenshot del error en la consola del navegador**
2. **Screenshot de la pestaña Network → Response del error**
3. **Output de estos comandos:**
   ```bash
   # En campus360-api-gateway
   cat .env | grep SECRET_KEY
   
   # En campus360-auth/campus360-auth-backend
   cat .env | grep SECRET_KEY
   
   # Versión de python-jose
   pip show python-jose
   ```

Con esa información podremos diagnosticar el problema exacto.

## 🎯 Resumen

Los cambios que hice deberían resolver el problema automáticamente. Lo más importante es:

1. ✅ **Hacer `git pull`** para obtener los cambios
2. ✅ **Limpiar localStorage** del navegador
3. ✅ **Verificar SECRET_KEY** en ambos `.env`
4. ✅ **Reiniciar todos los servicios**

El error ahora será mucho más específico y fácil de diagnosticar. 🚀
