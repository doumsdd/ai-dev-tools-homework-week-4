# Household Chores Manager

A Django web application for managing shared household chores among family members or roommates.

## Features

- **Task Management**: Create, edit, delete, and complete chores
- **Member Management**: Add household members and assign tasks to them
- **Dashboard**: Overview of pending tasks, overdue items, and task distribution
- **Task Rotation**: Automatically rotate tasks between members

## Tech Stack

- Python 3.x
- Django 5.x
- SQLite (development)
- Bootstrap CSS

## Installation

```bash
# Install dependencies
pip install django

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

## Usage

1. Navigate to `http://localhost:8000/`
2. Add household members
3. Create tasks and assign them to members
4. Track completion and manage chores

## Project Structure

```
django-todo/
├── config/          # Django project settings
├── todo/            # Main application
├── templates/       # HTML templates
├── _docs/           # Documentation
└── manage.py
```

## Development

```bash
# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate