🧾 Task Manager API

A fully functional Task Management API built using Django and Django REST Framework (DRF).
This API allows authenticated users to create, view, update, delete, and mark tasks as complete or incomplete.
A superuser (admin) can manage all users and their tasks through the Django Admin Dashboard.

🚀 Project Overview

The Task Manager API simulates a real-world backend system for managing personal or team tasks.
It supports:

User authentication via JWT (JSON Web Tokens)

User registration and login

Task CRUD operations (Create, Read, Update, Delete)

Task ownership control (users only see and manage their own tasks)

Admin control for managing all users and tasks

⚙️ Tech Stack

Backend Framework: Django 5.x

API Framework: Django REST Framework (DRF)

Authentication: JWT (via djangorestframework-simplejwt)

Database: SQLite (local) / PostgreSQL (production)

Deployment: Heroku / PythonAnywhere

📁 Project Structure
capstone_backend/
│
├── core/                  # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── tasks/                 # App handling task creation & management
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── users/                 # App handling user registration and authentication
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── manage.py
└── requirements.txt

🔑 Authentication Flow
1️⃣ Register a new user

POST → /api/register/

{
  "username": "john_doe",
  "password": "StrongPass123"
}

2️⃣ Login to get JWT tokens

POST → /api/token/

{
  "username": "john_doe",
  "password": "StrongPass123"
}


✅ Response:

{
  "refresh": "<your_refresh_token>",
  "access": "<your_access_token>"
}

3️⃣ Access protected endpoints

Add this header:

Authorization: Bearer <your_access_token>


Example:
GET → /api/tasks/

🧩 Task Endpoints
Method	Endpoint	Description	Auth Required
GET	/api/tasks/	List all your tasks	✅
POST	/api/tasks/	Create a new task	✅
GET	/api/tasks/<id>/	Retrieve a specific task	✅
PUT	/api/tasks/<id>/	Update a task	✅
PATCH	/api/tasks/<id>/	Partially update a task	✅
DELETE	/api/tasks/<id>/	Delete a task	✅
🧑‍💼 Admin Access

A Django superuser has been created to manage all users and tasks.

To log in to the Django admin panel:

URL: /admin/
Username: <your_superuser_username>
Password: <your_superuser_password>


To create your own superuser:

python manage.py createsuperuser

⚙️ Local Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/<your-username>/capstone_backend.git
cd capstone_backend

2️⃣ Create a virtual environment
python -m venv .venv
source .venv/Scripts/activate   # Windows
# or
source .venv/bin/activate       # macOS/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py migrate

5️⃣ Start the server
python manage.py runserver


Access locally:

http://127.0.0.1:8000/api/tasks/
