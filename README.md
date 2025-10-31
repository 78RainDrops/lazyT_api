# 📌 lazyT API

---

## overview

A minimalistic **Task Manager REST API** built with **Django** and **Django REST Framework (DRF)**.
This API allows authenticated users to create, view, edit, and delete their personal tasks all without a frontend.

---

## 🌐 Live API

**Render Deployment:**
👉 (https://lazyt-api.onrender.com)

Example endpoints:

- `https://lazyt-api.onrender.com/api/accounts/register/`
- `https://lazyt-api.onrender.com/api/task/`

---

## 🚀 Features

- 🔐 **JWT Authentication** (Custom implementation)
- 📝 **Creat, view, update and delete tasks**
- 🧩 **Filter and search** tasks by completion status, priority, and keywords
- ⚙️ **Pagination support**
- 🧠 **Custom error handling** and structured error responses
- 🧾 **Optimized queries** using `select_related()` and field indexing
- 🧰 **Auto-generated API documentation** using `drf-spectacular`

---

## 📁 Project Structure

```markdown
    lazyT_api/
    │
    ├── lazyT_api/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── tasks/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── authentication.py
    │   ├── migrations/
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── utils.py
    │   └── views.py
    │
    ├── manage.py
    ├── setup.py
    ├── requirements.txt
    ├── README.md
    └── .gitignore
```

---

## 🛠 Installation And Setup (Local)

![Python](https://img.shields.io/badge/python-3.12+-blue)  
![Django](https://img.shields.io/badge/Django-3.12+-blue)  
(just look or use the requirements.txt)

### Installation

## Clone the repository

```bash

git clone https://github.com/78RainDrops/lazyT_api.git
cd lazyT_api
```

## Set Up Virtual Environment

```bash
python -m venv .venv
source .venv/bin/acitvate # Linux/Mac
.venv\Scripts\activate # Windows

```

## Install Dependencies

```bash
pip install -r requirements.txt

```

## Configure environment variables

Create a `.env` file in the root directory:

```ini

SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=lazyt_db
DB_USER=lazyt_user
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1

```

For production (Render), add these in \*\*Render → Environment Varaibles:

```makefile

SECRET_KEY
DEBUG=False
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
ALLOWED_HOSTS=lazyt-api.onrender.com
```

---

## 🧪 Testing

Run tests using:

```bash
python manage.py test
```

Tests include:

- ✅ User registration and login
- ✅ JWT validation
- ✅ Task CRUD operations (create, read, update, delete)
- ✅ Error handling & missing fields

---

## 📡 API Endpoints

| Method     | Endpoint                  | Description                                | Auth Required |
| ---------- | ------------------------- | ------------------------------------------ | ------------- |
| **POST**   | `/api/accounts/register/` | Register a new user                        | ❌            |
| **POST**   | `/api/accounts/login/`    | Login and get JWT token                    | ❌            |
| **GET**    | `/api/task/`              | List all tasks (with filters & pagination) | ✅            |
| **POST**   | `/api/task/`              | Create a new task                          | ✅            |
| **GET**    | `/api/task/<id>/`         | Retrieve specific task                     | ✅            |
| **PUT**    | `/api/task/<id>/`         | Update task                                | ✅            |
| **DELETE** | `/api/task/<id>/`         | Delete task                                | ✅            |

---

## 🔎 Filters & Query Parameters

| Parameter   | Example           | Description                    |
| ----------- | ----------------- | ------------------------------ |
| `completed` | `?completed=true` | Filter completed tasks         |
| `priority`  | `?priority=high`  | Filter by priority level       |
| `search`    | `?search=project` | Search in title or description |
| `page`      | `?page=2`         | Pagination control             |

---

## ▶ Usage

### 🔐 Login

```bash

POST /api/accounts/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "12345"
}

```

---

### Response

```json
{
  "token": "your.jwt.token"
}
```

---

### Create Task

```bash

POST /api/task/
Authorization: Bearer your.jwt.token
Content-Type: application/json

{
  "title": "Finish project report",
  "description": "Complete the draft by Friday",
  "priority": "high"
}

```

---

### Mark Task as Completed

```bash

PUT /api/task/3/
Authorization: Bearer your.jwt.token
Content-Type: application/json

{
  "is_completed": true
}

```

---

## API Documentation

Once the server is running:

- Swagger UI: http://127.0.0.1:8000/api/schema/swagger-ui/
- ReDoc: http://127.0.0.1:8000/api/schema/redoc/

---

## Tech Stack

- **Backend:** Django 5.x
- **Framework:** Django REST Framework
- **Auth:** Custom JWT implementation
- **Docs:** drf-spectacular
- **Database:** PostgreSQL
- **Deploy:** Render

---

## 🧾 Version History

| Version  | Description                                                        |
| -------- | ------------------------------------------------------------------ |
| **v1.0** | Initial release – CRUD, JWT Auth, Custom Errors, Optimized Queries |
| **v1.1** | Deployment on Render + PostgreSQL + Static handling                |

---

## 🏷️ Version Tag

To tag this release:

```bash
git tag v1.1
git push origin v1.1
```

---

# 👨‍💻 Author

78RainDrops

[GitHub](https://github.com/78RainDrops)
