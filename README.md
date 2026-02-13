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

## Ejecución Local

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=notifier_db
```

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Motor**: Driver asíncrono de MongoDB
- **Pydantic**: Validación de datos con type hints
- **Uvicorn**: Servidor ASGI de alto rendimiento
