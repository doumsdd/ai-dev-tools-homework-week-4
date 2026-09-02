# Backlog - Personal Task Manager

## Task 1: Simplify Models
**Priority:** High  
**Status:** ✅ Done

Simplified the Task model for personal use:
- Removed Member model (no longer needed)
- Added priority field (high/medium/low)
- Kept: title, description, due_date, completed, completed_at, created_at

**Files modified:**
- `todo/models.py`

---

## Task 2: Update Views
**Priority:** High  
**Status:** ✅ Done

Updated views to remove member-related functionality:
- `home` - Dashboard with pending/completed tasks
- `task_list` - List all tasks
- `task_add` - Add a new task
- `task_edit` - Edit a task
- `task_delete` - Delete a task
- `task_complete` - Mark task as completed

**Files modified:**
- `todo/views.py`
- `todo/urls.py`

---

## Task 3: Update Templates
**Priority:** High  
**Status:** ✅ Done

Updated templates for the simplified app:
- `templates/base.html` - Updated navigation (removed members link)
- `templates/home.html` - Dashboard with priority badges
- `templates/tasks/list.html` - Task list with priority indicators
- `templates/tasks/add.html` - Add task form with priority selector
- `templates/tasks/edit.html` - Edit task form
- `templates/tasks/delete.html` - Delete confirmation
- Removed `templates/members/` directory

---

## Task 4: Update Admin
**Priority:** Medium  
**Status:** ✅ Done

Updated admin panel for Task model only.

**Files modified:**
- `todo/admin.py`

---

## Task 5: Update Tests
**Priority:** Medium  
**Status:** ✅ Done

Updated tests to match simplified model:
- 17 tests covering Task model, views, and priority functionality
- All tests passing ✅

**Files modified:**
- `todo/tests.py`

---

## Task 6: Database Reset
**Priority:** High  
**Status:** ✅ Done

Reset database to apply new schema:
- Deleted old migrations and database
- Created fresh migration `0001_initial.py`
- Applied all migrations

---

## Summary

The app has been simplified from a household chores manager to a personal task manager:
- **No more members** - tasks are personal
- **Priority system** - high (red), medium (yellow), low (green)
- **Clean UI** - Bootstrap with priority indicators
- **17 tests passing** ✅