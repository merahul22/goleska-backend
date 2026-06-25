# GO LESKA - Backend Services 

This is the backend for **GO LESKA**, an AI-powered, real-time hiring platform matching industrial/commercial employers with blue-collar workers via a 60-second dispatch paradigm.

Built with **FastAPI**, **SQLAlchemy 2.0**, **PostGIS** (via GeoAlchemy2), and **Redis** for real-time WebSocket dispatching.

---

##  Prerequisites

Before you begin, ensure you have the following installed on your machine:
- **Python 3.13+**
- **Docker Desktop** (Required for the PostGIS database and Redis)

---

##  Local Setup Instructions

Follow these exact steps to set up the backend environment after cloning the repository.

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd go-aleska/goleska-backend
```

### 2. Create and Activate the Virtual Environment
We use a standard Python virtual environment to manage dependencies.

**For Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
**For Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
Install all required packages from `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 4. Spin up the PostGIS Database
We use a Dockerized PostGIS instance to handle spatial queries (like calculating distances between workers and job sites).

Run the following command to start the database in the background on port `5433`:
```bash
docker run --name goleska-db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=goleska \
  -p 5433:5432 \
  -d postgis/postgis:16-3.4
```

### 5. Apply Database Migrations
We use Alembic to sync our SQLAlchemy Python models to the Postgres database. 

Run the migrations to create all the necessary tables (Employers, Workers, Jobs, etc.):
```bash
alembic upgrade head
```

### 6. Configure Your IDE (Optional but Recommended)
If you are using **VS Code** or **Cursor**, make sure you open the `goleska-backend` folder as your **Root Workspace** so the Python Language Server automatically detects the `.venv` and resolves imports like `sqlalchemy` properly.

---

##  Running the Server

Start the local development server with auto-reload:
```bash
fastapi dev app/main.py
```
*You can access the auto-generated Swagger documentation at: `http://localhost:8000/docs`*
