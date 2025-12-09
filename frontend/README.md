# CAMPUS360 Frontend

Frontend web para el sistema de autenticación CAMPUS360.

## 📁 Estructura

```
frontend/
├── index.html              # Página de login
├── css/
│   └── style.css          # Estilos globales
├── js/
│   └── utils.js           # Funciones utilitarias y API
└── pages/
    ├── register.html      # Registro de usuarios
    ├── dashboard.html     # Dashboard del usuario
    └── admin.html         # Panel de administración
```

## 🚀 Cómo Usar

### 1. Iniciar el Backend

Primero, asegúrate de que el servidor FastAPI esté corriendo:

```bash
cd ..
export PATH="$HOME/.local/bin:$PATH"
uvicorn app.main:app --reload
```

### 2. Abrir el Frontend

Abre el archivo `index.html` en tu navegador:

```bash
# Opción 1: Abrir directamente
open index.html  # macOS
xdg-open index.html  # Linux

# Opción 2: Usar un servidor HTTP simple
python3 -m http.server 8080
# Luego visita: http://localhost:8080
```

## 📱 Funcionalidades

### Para Usuarios

1. **Registro**: Crear una cuenta nueva
2. **Login**: Iniciar sesión con email y contraseña
3. **Dashboard**:
   - Ver credencial digital (QR)
   - Escanear ubicaciones
   - Ver historial de accesos

### Para Administradores

1. **Panel Admin**: Generar QRs de ubicaciones
2. **Descargar QRs**: Para imprimir y pegar en lugares físicos

## 🎨 Características

- ✅ Diseño moderno con gradientes
- ✅ Animaciones suaves
- ✅ Responsive design
- ✅ Manejo de errores
- ✅ Estados de carga
- ✅ Almacenamiento local de sesión

## 🔐 Seguridad

- JWT tokens almacenados en localStorage
- Auto-logout en caso de token inválido
- Validación de formularios
- Protección de rutas (requiere autenticación)
