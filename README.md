# 🛠️ Task Management System Backend

A robust Flask-based backend system for managing tasks with user authentication, role-based access, Redis caching, Celery task queues, PostgreSQL database, and Docker containerization.

---

## 🚀 Features

- ✅ User authentication and role-based access control (RBAC)
- 📂 CSV upload functionality for admins
- 🔐 JWT-based token authentication
- 🗄️ PostgreSQL for persistent task storage
- ⚡ Redis caching for filtered task queries
- 🧵 Celery + Redis for background task processing
- 🐳 Dockerized for easy deployment
- 🔒 Rate limiting & throttling for secure access

---

## 🏗️ Project Architecture

```text
📦 task-manager
├── app
│   ├── __init__.py         # App factory and extensions
│   ├── models.py           # SQLAlchemy models
│   ├── tasks.py            # Celery background tasks
├── api
│   └── __init__.py         # API routes and logic
├── scripts
│   └── init_db.py          # Database initialization script
├── config.py               # Environment-based config
├── Dockerfile              # Application container
├── docker-compose.yml      # Multi-container definition
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── API.adoc                # API Reference Guide
```
## ⚙️ Setup Instructions

### 1. 🔁 Clone the Repository
```bash
git clone https://github.com/your-username/task-manager.git
cd task-manager
```
### 2. 📦 Environment Variables
Create a .env file with the following:
```bash
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:yourpassword@db:5432/taskmanager
JWT_SECRET_KEY=your_jwt_secret
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```
### 3. 🐳 Start Services with Docker
```bash
docker exec -it mediaamp-web-1 bash
python scripts/init_db.py
```
### 4. 🧱 Initialize the Database
```bash
docker exec -it mediaamp-web-1 bash
python scripts/init_db.py
```

### 🔐 Authentication

```md
- `POST /register` – Register a new user
- `POST /login` – Login and receive a JWT token

Use the access token in the `Authorization` header:
Authorization: Bearer <your_token>
```
### 📬 API Overview
```bash
| Endpoint              | Method | Auth     | Role     | Description                         |
|----------------------|--------|----------|----------|-------------------------------------|
| `/register`          | POST   | ❌ No    | Public   | Register a new user                 |
| `/login`             | POST   | ❌ No    | Public   | Login and retrieve JWT token        |
| `/task`              | POST   | ✅ Yes   | User     | Create a new task                   |
| `/task/<id>`         | PUT    | ✅ Yes   | User     | Update a task                       |
| `/task/<id>`         | DELETE | ✅ Yes   | User     | Soft delete a task                  |
| `/task/<id>`         | GET    | ✅ Yes   | User     | Retrieve single task details        |
| `/tasks`             | GET    | ✅ Yes   | User     | Paginated list of all task logs     |
| `/upload-csv`        | POST   | ✅ Yes   | Admin    | Upload tasks in bulk via CSV        |

> 📘 See [`API.adoc`](./API.adoc) for detailed request/response examples
```
## ✅ Testing

You can test the API using tools like:

- [Postman](https://www.postman.com/)
- `curl`

### 🧪 Example using curl:

```bash
curl -X POST http://localhost:5000/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
```
## 📌 Notes
PostgreSQL DB persists using Docker volume

Redis cache clears on container restart

Ensure correct .env for JWT and DB secrets

✅ Use the provided CSV file from the company to test the /upload-csv endpoint. The system expects a well-formatted file with task data to uploaded by an admin.

📂 [sample_data/task_List.csv](./sample_data/task_List.csv)

## 📂 Contribution

Contributions and issues welcome! Fork this repo and raise a PR.

## 🔗 API Docs

📄 Read the full API Reference Guide in the [`API.adoc`](./API.adoc) file.

---

Built with ❤️ by Nishchal Sharma


