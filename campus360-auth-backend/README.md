# CAMPUS360 Authentication Module

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and update with your Supabase credentials:
```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL="your-supabase-postgresql-url"
SECRET_KEY="your-secret-key"
```

### 3. Generate Prisma Client & Create Tables
```bash
python -m prisma generate
python -m prisma db push
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

---

## 📋 API Endpoints

### Authentication
- **POST /auth/register** - Register new user
- **POST /auth/login** - Login and get JWT token

### QR Access (Protected 🔒)
- **GET /qr/me** - Get user profile for QR generation
- **POST /qr/scan** - Record location access
- **GET /qr/history** - Get access history

---

## 🏗️ Tech Stack
- **FastAPI** - Modern Python web framework
- **Prisma** - Type-safe ORM
- **Supabase** - PostgreSQL database
- **JWT** - Secure authentication
- **Bcrypt** - Password hashing

---

## 📁 Project Structure
```
campus360-auth/
├── prisma/
│   └── schema.prisma          # Database models
├── app/
│   ├── config.py              # Environment configuration
│   ├── main.py                # FastAPI app with Prisma lifecycle
│   ├── routers/
│   │   ├── auth.py            # Registration & login
│   │   └── qr_access.py       # QR scanning endpoints
│   ├── schemas/
│   │   └── schemas.py         # Pydantic models
│   └── utils/
│       └── auth_utils.py      # JWT & password utilities
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables (not in git)
```

---

## 🔐 Security Features
- ✅ Bcrypt password hashing
- ✅ JWT token authentication
- ✅ OAuth2 password flow
- ✅ Email uniqueness validation
- ✅ Protected endpoints with dependency injection

---

## 📚 Documentation
Full API documentation available at `/docs` when server is running.

For detailed implementation walkthrough, see [walkthrough.md](file:///home/srchaoz/.gemini/antigravity/brain/ce3e24ba-602f-4292-b129-8734280dc451/walkthrough.md)
