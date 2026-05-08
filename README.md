# CNC Tool Lifecycle Management Platform

Welcome to the CNC Tool Lifecycle Management Platform! This system is a robust, Django-based web application backed by Microsoft SQL Server (MSSQL), designed to track and manage the lifecycle, performance, and replacement metrics of CNC machining tools.

The entire project is **Dockerized**, meaning you can run it on any system (Windows, Mac, or Linux) with a single command, without worrying about manually installing Python, Django, or SQL Server.

---

## 🏗️ System Architecture & Database Structure

**Does this repository include the database structure?**
**Yes!** The GitHub repository includes all the database structures and sample data.
- The `database/` directory contains `.sql` scripts (e.g., `01_tables_overview.sql`, `02_table_schema.sql`, etc.) that define the tables, relationships, and seed data.
- When you run the application via Docker for the very first time, a dedicated initialization container (`init-db`) automatically waits for the SQL Server to boot up and executes all of these `.sql` scripts. 
- You do *not* need to create the database manually; the Docker setup handles the entire database initialization for you out of the box.

The core stack is:
- **Backend/Web**: Python 3.12, Django 4.2, `pyodbc`, `mssql-django`
- **Database**: Microsoft SQL Server 2022 (`mcr.microsoft.com/mssql/server:2022-latest`)
- **Containerization**: Docker & Docker Compose

---

## 🚀 Installation & Setup Guide (Windows / Mac)

Follow these step-by-step instructions to get the system running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed on your system:
1. **Git**: To clone the repository.
   - [Download Git](https://git-scm.com/downloads)
2. **Docker Desktop**: This handles running both the Django web server and the SQL Server database inside containers.
   - [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - *Note for Windows users*: Make sure WSL2 (Windows Subsystem for Linux) integration is enabled in Docker Desktop settings.

### Step 1: Clone the Repository

Open your terminal (Mac) or Command Prompt / PowerShell (Windows) and run:

```bash
git clone https://github.com/sumedhp23/cnc-tool-lifecycle-management.git
cd cnc-tool-lifecycle-management
```

### Step 2: Configure Environment Variables

The project uses a `.env` file to securely manage database credentials and Django settings. We have provided a template for you.

Copy the example file to create your own `.env` file:
- **On Mac/Linux:**
  ```bash
  cp .env.example .env
  ```
- **On Windows (Command Prompt):**
  ```cmd
  copy .env.example .env
  ```
*(You can also simply rename `.env.example` to `.env` in your file explorer).*

### Step 3: Build and Run the Containers

With Docker Desktop running, execute the following command in the terminal from the root of the project folder:

```bash
docker-compose up --build
```

**What happens during this step?**
1. Docker pulls the Python and Microsoft SQL Server images.
2. It builds the `web` container (installing the Microsoft ODBC drivers and Python dependencies from `requirements.txt`).
3. It starts the `db` (SQL Server) container.
4. Once the database is healthy, the `init-db` container runs automatically to execute all the SQL scripts located in the `database/` folder, structuring your tables and inserting sample data.
5. The `web` container starts the Django application.

*Note: The very first time you run this command, it might take a few minutes to download the Docker images and build the dependencies.*

### Step 4: Access the Application

Once you see logs indicating that the Django development server is running (`Starting development server at http://0.0.0.0:8000/`), open your web browser and go to:

👉 **http://localhost:8000**

You can also access the Django Administration panel at **http://localhost:8000/admin** to manage users, reports, and dynamic fields.

---

## 🛑 Stopping the Application

To stop the running application, go to the terminal where `docker-compose` is running and press:
`Ctrl + C`

To completely stop and remove the containers (your database data will persist in the Docker volume), run:
```bash
docker-compose down
```

## 🧹 Resetting the Database

If you ever want to completely wipe the database and start fresh, you can remove the Docker volumes:

```bash
docker-compose down -v
docker-compose up --build
```
*Warning: This will delete all data entered into the system since it was last initialized.*
