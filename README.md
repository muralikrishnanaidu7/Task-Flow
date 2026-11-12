# TaskFlow — Full-Stack Django Project & Task Manager

A multi-user full-stack web application built with **Python, Django, SQL (SQLite/PostgreSQL), HTML5, CSS3, and Vanilla JavaScript**.

## Features
- **User Authentication:** Registration, login, logout, and per-user data isolation.
- **Project & Task CRUD:** Create, view, edit, and delete projects and tasks.
- **Async Status Toggles:** Mark tasks complete or incomplete without full page reloads using the JavaScript `fetch()` API and CSRF protection.
- **Live Filtering & Search:** Instant client-side search and status filtering.
- **Responsive Design:** Clean, mobile-friendly UI built with custom CSS.

## Quick Setup
```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 4. Run development server
python manage.py runserver
```
Open `http://127.0.0.1:8000/` in your browser.
