# fastapi-caching-service

## Overview
This project is a caching service built using **FastAPI**. It leverages **PostgreSQL** for data storage and provides a RESTful API for transforming, interleaving, and caching payloads.

---

## Features
- **FastAPI** for building the RESTful API.
- **PostgreSQL** as the database for caching and storage.
- **Docker** and **Docker Compose** for containerization and deployment.
- Asynchronous database operations using `asyncpg` and `sqlalchemy[asyncio]`.
- Environment configuration with `python-dotenv`.

---

## Requirements
- **Python 3.10+** (if running locally)
- **PostgreSQL** (local or via Docker)
- **Docker** (optional for containerized setup)
- **Docker Compose**

## Setup

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd fastapi-caching-service.
```

## Usage
- Access the API documentation at `http://localhost:8000/docs` for interactive API exploration.
- Use the provided endpoints to interact with the caching service.

## Development




### **1. Configure Environment Variables**
- Create a .env file in the project root with the following content:

``` sh POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=caching_service
```
### **2. Set up a Python virtual environment**:
``` sh

  python3 -m venv venv
  source venv/bin/activate  # On Linux/macOS
  venv\Scripts\activate     # On Windows
```

### **3. Install dependencies**:
``` sh

  pip install -r requirements.txt


```


### **4. Build and Start Services locally**
``` bash
uvicorn app.main:app --reload
```
### **5 Verify the Application**
The FastAPI app will be available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### **6 Running Tests**
To run tests, use the following command:
```sh
pytest
```

## Usage
## Endpoints
### 1** Create Payload**
### **POST /payload**

- **Description**: This endpoint takes two lists of strings, transforms them (e.g., converts to uppercase), interleaves the elements, and caches the result.
- **Request Body**:
``` json

  {
    "list_1": ["first string", "second string", "third string"],
    "list_2": ["other string", "another string", "last string"]
  }
```
- **Response**:
``` json

  {
    "id": "a_unique_payload_id",
    "output": "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING, THIRD STRING, LAST STRING"
  }
``` 
- **Error Response**:
``` json

  {
    "detail": "Invalid input. Ensure both lists are of equal length."
  }
``` 
### 2** Retrieve Payload**
- **GET /payload/{id}**

- **Description**: Fetch a cached payload using its unique identifier.
- **Path Parameter**:
-- id (string): The unique identifier for the payload.
-- **Response**:
``` json
  
  {
    "id": "a_unique_payload_id",
    "output": "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING, THIRD STRING, LAST STRING"
  }
```

- **Error Response**:
``` json


  {
    "detail": "Payload not found"
  }
```
- **Example Usage**
- **POST /payload (via curl)**

## fastapi-caching-service/
``` bash
├── app/
│   ├── __init__.py               # Package initializer
│   ├── database.py               # Database configuration
│   ├── models.py                 # SQLAlchemy models
│   ├── schemas.py                # Pydantic schemas
│   ├── services.py               # Core business logic
│   ├── main.py                   # FastAPI app entry point
├── tests/
│   ├── __init__.py               # Test package initializer
│   ├── conftest.py               # Shared pytest fixtures
│   ├── test_database.py          # Database tests
│   ├── test_models.py            # Tests for models
│   ├── test_services.py          # Tests for business logic
│   ├── test_endpoints.py         # API endpoint integration tests
│   ├── test_env.py               # Tests for environment variables
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
├── README.md                     # Documentation
```

