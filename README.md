# 🧠 MindInk
MindInk is a Django-based REST API that allows users to manage personal notes with secure JWT-based authentication. It includes user signup/login/logout, password reset, and CRUD functionality for notes.

## 🚀 Features

- User Registration & Login, Logout with JWT
- Password Reset
- Notes CRUD API (Create, Read, Update, Delete)
- Unit Tests
- Dockerized setup with PostgreSQL

---
##🛠️ Installation
1.  **Clone the repository**
```bash
git clone git@github.com:PritomKarmokar/mindInk.git
cd mindInk
```
2. **Copy `.env.example` to `.env`**
```bash
cp .env.example .env
```
- 📌 Make sure to update the .env file with the correct values
3. **Create & Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
4.  **Install Dependencies**
```bash
pip install -r requirements.txt 
```
5. **Setup the Database**
```bash
python manage.py migrate
```
6. **Create Superuser(optional)**
```bash
python manage.py createsuperuser
```
7. **Run the development server**
```bash
python manage.py runserver
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

> ⚠️ All notes endpoints require JWT in the Authorization header:
```makefile
Authorization: Bearer <access_token>
```
