# Plan - Personal Task Manager

## Overview

A simple personal task management application built with Django.

**Purpose:** Track personal work/study tasks with priority levels.  
**Users:** Single person (no multi-user/member features).

---

## Requirements (as agreed)

| Requirement | Decision |
|-------------|----------|
| Main purpose | Personal task tracking |
| Task types | Work/study tasks |
| Organization | By priority (high/medium/low) |
| Recurring tasks | No - only one-time tasks |
| Members | Removed - single user app |

---

## Data Model

### Task

| Field | Type | Description |
|-------|------|-------------|
| title | CharField(200) | Task title (required) |
| description | TextField | Optional description |
| priority | CharField(10) | `high`, `medium`, `low` (default: medium) |
| due_date | DateField | Optional due date |
| completed | BooleanField | Completion status (default: false) |
| completed_at | DateTimeField | When task was completed |
| created_at | DateTimeField | Auto-set on creation |

**Ordering:** By priority (high first), then due_date, then title.

---

## Features

### Dashboard (Home)
- View pending tasks with priority badges
- View completed tasks count
- Quick actions: Add task, View all tasks

### Task Management
- **List** - View all tasks in a table with priority indicators
- **Add** - Create new task with title, description, priority, due date
- **Edit** - Modify existing task
- **Delete** - Remove task with confirmation
- **Complete** - Mark task as done

### Priority System
- **High** (red badge) - Urgent tasks
- **Medium** (yellow badge) - Normal priority (default)
- **Low** (green badge) - Can wait

---

## URLs

| Path | View | Name |
|------|------|------|
| `/` | home | Dashboard |
| `/tasks/` | task_list | All tasks |
| `/tasks/add/` | task_add | Add task |
| `/tasks/<pk>/edit/` | task_edit | Edit task |
| `/tasks/<pk>/delete/` | task_delete | Delete task |
| `/tasks/<pk>/complete/` | task_complete | Mark done |
| `/admin/` | Django admin | Admin panel |

---

## Templates

```
templates/
├── base.html          # Base layout with navigation
├── home.html          # Dashboard
└── tasks/
    ├── list.html      # All tasks table
    ├── add.html       # Add task form
    ├── edit.html      # Edit task form
    └── delete.html    # Delete confirmation
```

---

## Testing

17 unit tests covering:
- Task model creation and methods
- Priority functionality
- All view responses (GET/POST)
- Task completion workflow

**Run tests:**
```bash
python manage.py test
```

---

## Setup & Running

```bash
# Install dependencies
pip install django

# Apply migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Access at: http://127.0.0.1:8000/  
Admin at: http://127.0.0.1:8000/admin/

---

## Future Enhancements (optional)

- [ ] Task categories/tags
- [ ] Search and filter tasks
- [ ] Export tasks to CSV
- [ ] Dark mode toggle
- [ ] Task reminders/notifications