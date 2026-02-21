# Mini Blog API

A REST API for a blog application : with FastAPI and PostgreSQL.  
**[Live_demo](https://fastapi-blog-hneb.onrender.com)**

## Tech Stack

- Python 3.12 / FastAPI
- PostgreSQL (database)
- SQLAlchemy (orm)
- Alembic (migrations/updates models)
- JWT (authentication)
- Docker (deployment)
- Pytest 

## Features

### Models
- Soft delete system
- status (active, archived, signaled)
- Role-based control (ie: only owner can delete a post)

#### Users
- registration
- authentication with JWT token


#### Posts
- CRUD 
- separated services/routes 
- pagination for posts listing

**Automated tests with pytest**


## How to run

### Prerequisites
- Docker
- Docker compose

### Setup

1. Clone the repository
```bash 
git clone https://github.com/Dr00pyd00/First_Mini_Blog_API
cd First_Mini_Blog_API
```

2. Create '.env' file
```bash
cp .env.example .env
# fill this with yours values 
```

3. Start Docker containers
```bash
docker compose up --build
```

4. Run Alembic migrations for tables in database
```bash 
docker compose exec api alembic upgrade head
```

5. API working on `http://localhost:8000`

## Documentation

Interactive and testable doc at:
- Swagger :`https://fastapi-blog-hneb.onrender.com/docs`
- ReDoc `https://fastapi-blog-hneb.onrender.com/redoc`
