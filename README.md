# Universal Notifier API

Sistema de notificaciones multi-canal construido con FastAPI, MongoDB y Docker.

## Estructura del Proyecto

```
Universal-Notifier-API/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point de la aplicación
│   ├── core/
│   │   ├── config.py        # Configuración y variables de entorno
│   │   └── database.py      # Conexión a MongoDB
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/   # Endpoints REST
│   ├── models/              # Modelos de datos (MongoDB)
│   └── schemas/             # Schemas Pydantic (validación)
├── requirements.txt
└── .gitignore
```

## Requisitos

- Python 3.11+
- MongoDB
- Docker (opcional)

## Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 🚀 Ejecución con Docker (Recomendado)

### Iniciar todos los servicios

```bash
docker-compose up -d
```

Esto levantará:
- **API FastAPI** en http://localhost:8000
- **MongoDB** en puerto 27017
- **API Docs** en http://localhost:8000/docs

### Ver logs

```bash
docker-compose logs -f api
```

### Detener servicios

```bash
docker-compose down
```

### Reconstruir después de cambios

```bash
docker-compose up -d --build
```

### Opcional: Levantar con MongoDB Express (UI)

```bash
docker-compose --profile debug up -d
```

MongoDB Express estará en http://localhost:8081 (usuario: `admin`, password: `admin123`)

## 🐍 Ejecución Local (sin Docker)

### 1. Instalar dependencias

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copiar `.env.example` a `.env` y ajustar:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=notifier_db
```

### 3. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentación API

Una vez iniciada la aplicación, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints disponibles:

#### Notificaciones (v1)

- **POST** `/api/v1/notifications/` - Crear nueva notificación
- **GET** `/api/v1/notifications/` - Listar notificaciones (con paginación y filtros)
- **GET** `/api/v1/notifications/{id}` - Obtener notificación por ID
- **PATCH** `/api/v1/notifications/{id}` - Actualizar notificación
- **DELETE** `/api/v1/notifications/{id}` - Eliminar notificación

#### Canales soportados:
- `email` - Email
- `sms` - SMS
- `push` - Push notification
- `webhook` - Webhook
- `slack` - Slack
- `telegram` - Telegram

#### Estados de notificación:
- `pending` - Pendiente de envío
- `sent` - Enviada exitosamente
- `failed` - Falló el envío
- `cancelled` - Cancelada

#### Prioridades:
- `low` - Baja
- `normal` - Normal (default)
- `high` - Alta
- `urgent` - Urgente

### Ejemplo de uso:

```bash
# Crear notificación
curl -X POST http://localhost:8000/api/v1/notifications/ \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "email",
    "recipient": "user@example.com",
    "subject": "Welcome!",
    "message": "Welcome to Universal Notifier API",
    "priority": "high",
    "metadata": {"user_id": "123"}
  }'

# Listar notificaciones (con filtros)
curl http://localhost:8000/api/v1/notifications/?status=pending&page=1&page_size=10

# Actualizar estado
curl -X PATCH http://localhost:8000/api/v1/notifications/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "sent"}'
```

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Motor**: Driver asíncrono de MongoDB
- **Pydantic**: Validación de datos con type hints
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Docker**: Containerización y orquestación
