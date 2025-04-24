# 🧠 MindInk
- MindInk is a Django-based REST API for managing personal notes with secure JWT authentication. 
- It includes user registration, login/logout, password reset, and full CRUD operations for notes. Dockerized with PostgreSQL for easy deployment.

---

## 🚀 Features

- 🔐 JWT Authentication (Signup, Login, Logout)
- 🔁 Password Reset (Request & Change)
- 📝 Notes CRUD (Create, Read, Update, Delete)
- 🧪 Unit Testing
- 🐳 Dockerized with PostgreSQL

---

## ⚙️ Local Setup

1. **Clone & Navigate**
```bash
git clone git@github.com:PritomKarmokar/mindInk.git
cd mindInk
```
2. **Copy `.env.example` to `.env`**
```bash
cp .env.example .env
# Update `.env` with DB credentials & secret key
```
3. **Create & Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
4. **Install Dependencies**
```bash
pip install -r requirements.txt 
```
5. **Database & Server**
```bash
python manage.py migrate
python manage.py runserver
```
6. **(Optional) Create Admin & Run Tests**
```bash
python manage.py createsuperuser
python manage.py test
```
## 🔐 Auth API Endpoints (JWT)

| Method | Endpoint                         | Description                    |
|--------|----------------------------------|--------------------------------|
| POST   | `/signup/`                       | User signup                    |
| POST   | `/login/`                        | User login → returns JWT token |
| POST   | `/logout/`                       | User logout                    |
| POST   | `/reset-password-request/`       | Request password reset         |
| GET    | `/reset-password/<token>/`       | Access reset password page     |
| POST   | `/reset-password/<token>/`       | Change password                |


## 📝 Notes API Endpoints (Authenticated)

| Method | Endpoint         | Description              |
|--------|------------------|--------------------------|
| GET    | `/home/`         | Welcome/Home endpoint    |
| GET    | `/`              | List all notes           |
| POST   | `/`              | Create a new note        |
| GET    | `/<note_id>/`    | Retrieve a note by ID    |
| PUT    | `/<note_id>/`    | Update a note            |
| DELETE | `/<note_id>/`    | Delete a note            |

> ⚠️ All endpoints require::
```makefile
Authorization: Bearer <access_token>
```
## 🐳 Docker Setup
- **Build & Run**
```bash
docker compose up --build
```
- **Run Migrations & Superuser**
- Open another terminal and run the below commands:
```bash
docker exec -it mindInk python manage.py migrate
docker exec -it mindInk python manage.py createsuperuser
```
-  **Run Tests**
```bash
docker exec -it mindInk python manage.py test
```