"""
# Mini Sistema de Créditos Backend

Este proyecto implementa un sistema de gestión de créditos con FastAPI y MongoDB, proporcionando endpoints para la solicitud y gestión de créditos, así como la generación y consulta de planes de amortización.

## Requisitos previos

- Python (v3.8+)
- FastAPI (v3.0.0+)
- MongoDB (v4.4+)
- PyJWT (v2.3.0+)
- Motor (v2.5.1+)
- dotenv (v0.19.1+)
- pymongo (v4.0.1+)
- fastapi-pagination (v0.6.0+)

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/cedioza/mini-sistema-creditos
   cd mini-sistema-creditos-backend

2. Crea un entorno virtual (opcional pero recomendado):

   ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

3. Instala las dependencias:

   ```bash
    pip install -r requirements.txt


5. Configura las variables de entorno:

    Crea un archivo .env en la raíz del proyecto y define las siguientes variables:
   ```bash
    MONGODB_URL = "mongodb://utxvyhitcd3fa1y45lj2:l3sRGFQS0xtm5fbmXNU2@n1-c2-mongodb-clevercloud-customers.services.clever-cloud.com:27017,n2-c2-mongodb-clevercloud-customers.services.clever-cloud.com:27017/bvo3gs2et2wyhzl?replicaSet=rs0"
    DATABASE = 'bvo3gs2et2wyhzl'
    COLLECTION_AMORTIZACION = 'amortizacion'
    POSTGRESQL_DB = "postgresql://uhdnzllwcyup89iy4myr:WBbGKqbTmG439dXGh4hyni4DMU2ba0@blgowgn0o6bwkrgxxw07-postgresql.services.clever-cloud.com:50013/blgowgn0o6bwkrgxxw07"
    SECRET_KEY = '4d2a8c1f7e823de5a2b8453c2ae479d39f9b4bc3e6d6c7d9a7f6c896923456'

6. Inicia el servidor de desarrollo::

   ```bash
    uvicorn main:app --reload


## Estructura del Proyecto


    /mini-sistema-creditos
    │
    ├── app
    │   ├── main.py          # Punto de entrada de FastAPI
    │   ├── auth.py          # Autenticación
    │   ├── models.py        # Modelos para la base de datos
    │   ├── schemas.py       # Esquemas para validación de datos
    │   ├── crud.py          # Operaciones CRUD
    │   ├── amortizacion.py  # Lógica de amortización
    │   ├── database.py      # Configuración de la base de datos
    │   └── ...
    ├── requirements.txt     # Dependencias de Python
    └── ...

    main.py: Punto de entrada de la aplicación FastAPI.
    models.py: Definición de los modelos de datos usando Pydantic.
    database.py: Configuración de la conexión a la base de datos MongoDB.
    crud.py: Operaciones CRUD para interactuar con la base de datos.
    schemas/: Esquemas Pydantic para validación de datos.
    Funcionalidades
    Autenticación y Autorización: Utilización de JWT para autenticación segura de usuarios.
    Endpoints de Créditos: Gestión de solicitudes y aprobaciones de créditos.
    Planes de Amortización: Generación y consulta de planes de amortización para cada crédito.
    Validación de Datos: Uso extensivo de esquemas Pydantic para la validación de datos de entrada y salida.
