# Kanmind Backend

This repository contains the backend of "Kanmind" (task management app from the Developer Akademie).
This Backend is built with Python and Django REST Framework, handling authentication, board/task management, and persistent data storage.

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)   
- [License](#license)  

## Features

- User authentication and role management  
- CRUD operations for projects and tasks  
- RESTful API endpoints for frontend integration  
- PostgreSQL database for persistent storage  
- Input validation and error handling  

## Tech Stack

- **Language:** Python 3.x  
- **Framework:** Django 5.2.8  
- **REST Framework:** Django REST Framework 3.16.1  
- **Database:** PostgreSQL  
- **Linting / Code Quality Tools:**  
  - `mccabe` 0.7.0  
  - `pycodestyle` 2.14.0  
  - `pyflakes` 3.4.0  
  - `ruff` 0.14.6  
- **Utilities:** `asgiref`, `sqlparse`, `tzdata`  

## Getting Started

Follow these steps to set up a local development environment:

### Prerequisites

- Python 3.11+  
- pip  
- PostgreSQL database  
- Git  

### Clone the Repository

```bash
git clone https://github.com/anitagasteiner/kanmind.git
```

### Create Virtual Environment

```bash
cd kanmind
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Migration
    
```bash
python manage.py migrate
```

### Run Server

```bash
python manage.py runserver
```

### Create Superuser (optional)

```bash
python manage.py createsuperuser
```

## API Documentation

The backend exposes RESTful endpoints under /auth/ and /api/, including:

| API Endpoint | Description |
| --------------- | -------------- |
| '/api/registration' | registration and token management |
| '/api/login' | login |
| '/api/boards/' | boards CRUD operations |
| '/api/tasks/' | tasks CRUD operations |

## License

This project is licensed under the MIT License. See LICENSE.txt for details.


