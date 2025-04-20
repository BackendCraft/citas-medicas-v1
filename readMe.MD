# Documentación: Sistema de Citas Médicas (citas-medicas-v1)

## Índice
1. [Descripción general](#descripción-general)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Estructura del proyecto](#estructura-del-proyecto)
5. [Configuración](#configuración)
6. [Aplicaciones](#aplicaciones)
7. [API REST](#api-rest)
8. [Sistema de suscripciones](#sistema-de-suscripciones)
9. [Despliegue](#despliegue)
10. [Contribuir](#contribuir)

## Descripción general

Este proyecto es un sistema de gestión de citas médicas desarrollado con Django 5.2. La aplicación permite administrar pacientes y gestionar suscripciones mediante la integración con Stripe para procesamiento de pagos.

## Requisitos

- Python 3.x
- Django 5.2
- Django REST Framework 3.16.0
- Stripe 12.0.0
- Otros requisitos están especificados en `requirements.txt`

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/citas-medicas-v1.git
   cd citas-medicas-v1
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno (especialmente las claves de Stripe):
   - `STRIPE_PUBLISHABLE_KEY`
   - `STRIPE_SECRET_KEY`

5. Aplica las migraciones:
   ```bash
   python manage.py migrate
   ```

6. Crea un superusuario:
   ```bash
   python manage.py createsuperuser
   ```

7. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Estructura del proyecto

El proyecto está organizado con la siguiente estructura:

```
citas-medicas-v1/
├── citas/                  # Configuración del proyecto principal
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Configuración general
│   ├── urls.py             # URLs del proyecto
│   └── wsgi.py
├── pacientes/              # Aplicación para gestión de pacientes
├── suscripciones/          # Aplicación para gestión de suscripciones
├── manage.py
└── requirements.txt        # Dependencias del proyecto
```

## Configuración

### Configuración principal (settings.py)

El archivo `citas/settings.py` contiene la configuración principal del proyecto:

- Base de datos: SQLite por defecto
- Aplicaciones instaladas: 
  - Django admin
  - Django auth
  - REST Framework
  - Pacientes
  - Suscripciones
- Configuración de Stripe para pagos

### URLs (urls.py)

El archivo `citas/urls.py` define las rutas principales:

- `/admin/`: Panel de administración de Django
- `/accounts/`: Sistema de autenticación
- `/`: Rutas principales de la aplicación de pacientes
- `/suscripciones/`: Rutas para el sistema de suscripciones

## Aplicaciones

### Pacientes

Esta aplicación maneja la gestión de pacientes y citas médicas. Incluye:

- Modelos para pacientes y citas
- Vistas para crear, leer, actualizar y eliminar información
- Formularios para la entrada de datos
- Templates para la interfaz de usuario

### Suscripciones

Esta aplicación gestiona las suscripciones y pagos a través de Stripe:

- Modelos para planes y suscripciones
- Integración con la API de Stripe
- Webhooks para procesar eventos de Stripe
- Sistema de gestión de pagos recurrentes

## API REST

El proyecto utiliza Django REST Framework para proporcionar una API RESTful:

- Endpoints para gestionar pacientes
- Endpoints para gestionar suscripciones
- Autenticación y permisos
- Serialización de datos

Para usar la API, se necesita autenticación. Consulta la sección específica de cada aplicación para más detalles sobre los endpoints disponibles.

## Sistema de suscripciones

El sistema de suscripciones está integrado con Stripe y permite:

- Crear planes de suscripción
- Gestionar clientes
- Procesar pagos
- Manejar renovaciones automáticas
- Cancelar suscripciones

### Configuración de Stripe

El proyecto utiliza las siguientes claves de Stripe para el entorno de pruebas:

```python
STRIPE_PUBLISHABLE_KEY = 'pk_test_...'
STRIPE_SECRET_KEY = 'sk_test_...'
```

**Importante**: Para producción, reemplaza estas claves con tus claves reales y configúralas como variables de entorno.

## Despliegue

Para desplegar este proyecto en producción:

1. **Configuración de seguridad**:
   - Cambia `DEBUG = False` en `settings.py`
   - Genera una nueva `SECRET_KEY`
   - Configura `ALLOWED_HOSTS` adecuadamente
   - Utiliza variables de entorno para las claves sensibles

2. **Base de datos**:
   - Para producción, considera usar PostgreSQL o MySQL en lugar de SQLite
   - Configura las credenciales de la base de datos en `settings.py`

3. **Archivos estáticos**:
   - Configura `STATIC_ROOT` y ejecuta `python manage.py collectstatic`
   - Considera usar un CDN o servidor web para servir archivos estáticos

4. **Servidor web**:
   - Configura un servidor como Nginx o Apache
   - Utiliza Gunicorn o uWSGI como servidor WSGI

## Contribuir

Si deseas contribuir a este proyecto:

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva característica'`)
4. Sube los cambios a tu fork (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

---

Desarrollado por Luis Fernández usando Django 5.2
