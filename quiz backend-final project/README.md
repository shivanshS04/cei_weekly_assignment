# Quiz Backend Management API

A RESTful backend API for creating and managing quiz questions and answer choices, built with **FastAPI**, **SQLAlchemy**, and **Pydantic**.

---

## Tech Stack

| Technology    | Purpose                              |
|---------------|--------------------------------------|
| FastAPI       | Building RESTful APIs                |
| SQLAlchemy    | Database ORM and management          |
| Pydantic v2   | Data validation and serialization    |
| SQLite        | Database storage (`quiz.db`)         |
| Uvicorn       | ASGI server for running FastAPI      |

---

## Project Structure

```
final_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLAlchemy engine & session
│   ├── models.py            # ORM models (Question, Choice)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── crud.py              # Business logic / CRUD operations
│   └── routers/
│       ├── __init__.py
│       ├── questions.py     # Question endpoints
│       └── choices.py       # Choice endpoints
├── seed_data.py             # Seed database with 60 sample questions
├── requirements.txt
└── README.md
```

---

## Database Design

### Question Table

| Field         | Type    | Description              |
|---------------|---------|--------------------------|
| id            | Integer | Primary Key              |
| question_text | String  | The quiz question        |
| category      | String  | Category/domain (optional)|

### Choice Table

| Field       | Type    | Description                        |
|-------------|---------|------------------------------------|
| id          | Integer | Primary Key                        |
| choice_text | String  | Answer option text                 |
| is_correct  | Boolean | Indicates the correct answer       |
| question_id | Integer | Foreign Key → questions.id         |

**Relationship**: One Question → Many Choices (cascade delete)

---

## Setup & Installation

### 1. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed the database (optional but recommended)

```bash
python seed_data.py
```

This populates the database with **60 sample questions** across 6 categories (10 each):
- General Knowledge
- Programming
- Mathematics
- Data Science
- Business Studies
- Aptitude

### 4. Start the server

```bash
uvicorn app.main:app --reload
```

The server will start at: **http://127.0.0.1:8000**

---

## API Documentation

Once the server is running, visit:

- **Swagger UI** (interactive): http://127.0.0.1:8000/docs
- **ReDoc** (reference): http://127.0.0.1:8000/redoc

---

## API Endpoints

### Question Endpoints

| Method   | Endpoint              | Description                               |
|----------|-----------------------|-------------------------------------------|
| `POST`   | `/questions`          | Create a new question                     |
| `GET`    | `/questions`          | Get all questions (supports filters)      |
| `GET`    | `/questions/{id}`     | Get a specific question by ID             |
| `PUT`    | `/questions/{id}`     | Update an existing question               |
| `DELETE` | `/questions/{id}`     | Delete question + all its choices         |

**Query Parameters for `GET /questions`:**
- `category` — Filter by category name (e.g., `Programming`)
- `skip` — Pagination offset (default: 0)
- `limit` — Max records returned (default: 100)

### Choice Endpoints

| Method   | Endpoint          | Description                         |
|----------|-------------------|-------------------------------------|
| `POST`   | `/choices`        | Create a new answer choice          |
| `GET`    | `/choices`        | Get all choices (supports filters)  |
| `GET`    | `/choices/{id}`   | Get a specific choice by ID         |
| `PUT`    | `/choices/{id}`   | Update an existing choice           |
| `DELETE` | `/choices/{id}`   | Delete an answer choice             |

**Query Parameters for `GET /choices`:**
- `question_id` — Filter choices by question ID
- `skip` — Pagination offset (default: 0)
- `limit` — Max records returned (default: 100)

---

## Example Requests

### Create a Question

```json
POST /questions
{
  "question_text": "What is the capital of India?",
  "category": "General Knowledge"
}
```

### Add Choices to the Question

```json
POST /choices
{
  "choice_text": "New Delhi",
  "is_correct": true,
  "question_id": 1
}
```

### Get All Programming Questions

```
GET /questions?category=Programming
```

### Update a Question

```json
PUT /questions/1
{
  "category": "Geography"
}
```

### Delete a Question (and all its choices)

```
DELETE /questions/1
```

---

## Pydantic Schemas

```python
# As specified in the project document
class QuestionCreate(BaseModel):
    question_text: str
    category: str | None = None
```

---

## System Architecture

```
Client Request
     ↓
 FastAPI Routes (routers/)
     ↓
 Business Logic Layer (crud.py)
     ↓
 SQLAlchemy ORM (models.py)
     ↓
 SQLite Database (quiz.db)
```
