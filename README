# 🚀 LinkUp – Personal Portfolio API

**LinkUp** is a LinkedIn-inspired RESTful API designed to manage and showcase professional portfolios. It enables users to present their skills, experiences, and projects in a structured and scalable format. The platform provides public endpoints to explore user profiles and private routes for managing personal data.

## 📌 Overview

This API allows users to:

* Create and manage professional profiles
* Showcase projects and experiences
* Associate skills across projects and experiences without duplication
* Access public user portfolios

It is built using modern backend technologies and follows best practices for scalable system design.

---

## ✨ Features

* 🔐 Authentication and User Account Management
* 👤 Public User Profiles
* 🛠️ Skills Management with Deduplication
* 💼 Experience Tracking
* 📁 Project Showcasing
* 🔗 Many-to-Many Relationships Between Skills, Projects, and Experiences
* 📄 RESTful API Design
* 📦 Dockerized Deployment
* 🗄️ SQLite Database Integration
* 📚 Automatic API Documentation with Swagger and ReDoc

---

## 🏗️ Tech Stack

| Technology | Purpose            |
| ---------- | ------------------ |
| FastAPI    | Backend Framework  |
| SQLAlchemy | ORM                |
| Pydantic   | Data Validation    |
| SQLite     | Database           |
| Docker     | Containerization   |
| Uvicorn    | Application Server |
| Pytest     | Testing            |

---

## 📂 Project Structure

```bash
Personal_Portfolio_API/
│── app/
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── services.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── skill.py
│   │   ├── experience.py
│   │   ├── project.py
│   │   └── association_tables.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── skill.py
│   │   ├── experience.py
│   │   ├── project.py
│   │   └── profile.py
│   │
│   └── routers/
│       ├── auth.py
│       ├── user.py
│       ├── user_account.py
│       ├── skills.py
│       ├── experience.py
│       └── project.py
│
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── linkup.db
```

---

## 🗄️ Database Design

### Entities

* **User**
* **Skill**
* **Project**
* **Experience**

### Relationships

| Relationship        | Type         |
| ------------------- | ------------ |
| User ↔ Skills       | Many-to-Many |
| User ↔ Projects     | One-to-Many  |
| User ↔ Experiences  | One-to-Many  |
| Project ↔ Skills    | Many-to-Many |
| Experience ↔ Skills | Many-to-Many |

This design ensures **no duplicate skills**, as skills are reused across projects and experiences.

---

## 📊 Sample API Response

```json
{
  "name": "max",
  "projects": [
    {
      "title": "sdf",
      "description": "ert",
      "skills": [
        { "name": "python" }
      ]
    }
  ],
  "experiences": [
    {
      "role": "odoo",
      "company": "sdf",
      "skills": [
        { "name": "odoo" },
        { "name": "sql" }
      ]
    }
  ],
  "skills": [
    { "name": "python" },
    { "name": "django" },
    { "name": "sql" }
  ]
}
```

---

## ⚙️ Installation and Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/linkup-api.git
cd linkup-api
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./linkup.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

---

## 📘 API Documentation

Once the server is running:

* **Swagger UI:**
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* **ReDoc:**
  [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🐳 Running with Docker

### Build and Run

```bash
docker-compose up --build
```

Stop containers:

```bash
docker-compose down
```

---

## 🔑 API Endpoints

### Authentication

* `POST /auth/register`
* `POST /auth/login`

### Users

* `GET /users` – List all users (Public)
* `GET /users/{id}` – Get user profile (Public)

### Skills

* `POST /skills`
* `GET /skills`

### Projects

* `POST /projects`
* `GET /projects`

### Experiences

* `POST /experiences`
* `GET /experiences`

### User Account

* `GET /account/profile`
* `PUT /account/profile`

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📜 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author

**Khushi Koriya**


GitHub: [https://github.com/khushiiik]

---