# Backlog — Personal Task Manager

> Generated from `_docs/plan.md`. The core MVP (model, views, templates, admin, 17 tests) is complete.
> The tasks below are the proposed next steps, ordered by priority.

---

## Task 1 — Django Forms & CSRF Hardening
**Priority:** High · **Status:** 🔲 To Do

Replace manual `request.POST.get(...)` handling in `task_add` / `task_edit` with a proper `ModelForm` for validation and cleaner code.

**Acceptance criteria**
- New `todo/forms.py` with a `TaskForm` (ModelForm for `Task`).
- `task_add` and `task_edit` use `TaskForm`; invalid submissions re-render the form with inline errors.
- Existing 17 tests still pass; add tests for invalid submissions (empty title, bad priority value).

**Files touched:** `todo/forms.py` *(new)*, `todo/views.py`, `templates/tasks/add.html`, `templates/tasks/edit.html`, `todo/tests.py`.

---

## Task 2 — Task Categories / Tags
**Priority:** High · **Status:** 🔲 To Do

Allow each task to be tagged with one or more categories (e.g. *Work*, *Study*, *Personal*).

**Acceptance criteria**
- New `Category` model (`name` CharField, optional `color` CharField).
- M2M relationship `Task.categories`.
- Category filter dropdown on the task-list and dashboard views.
- Category pills shown next to priority badges in templates.
- Admin panel updated to manage categories.
- At least 3 new unit tests (create category, assign to task, filter by category).

**Files touched:** `todo/models.py`, `todo/views.py`, `todo/urls.py`, `todo/admin.py`, `todo/tests.py`, templates, new migration.

---

## Task 3 — Search & Filter
**Priority:** High · **Status:** 🔲 To Do

Add a search box and filter controls so the user can quickly find tasks.

**Acceptance criteria**
- Text search across `title` and `description` (query param `?q=`).
- Filter by priority (`?priority=high|medium|low`).
- Filter by status (`?status=pending|completed|all`).
- Filters are composable and reflected in the URL (bookmarkable).
- "Clear filters" link resets to the default list.
- At least 4 unit tests covering each filter and combined filters.

**Files touched:** `todo/views.py` (update `task_list`), `templates/tasks/list.html`, `todo/tests.py`.

---

## Task 4 — Task Overdue Indicator
**Priority:** Medium · **Status:** 🔲 To Do

Visually flag overdue tasks and add a "due soon" section on the dashboard.

**Acceptance criteria**
- Tasks whose `due_date < today` and `completed == False` show a red "Overdue" badge.
- Dashboard gains an "Upcoming / Overdue" card listing tasks due within the next 7 days.
- `Task.is_overdue` property added to the model.
- At least 2 unit tests for `is_overdue`.

**Files touched:** `todo/models.py`, `todo/views.py`, `templates/home.html`, `templates/tasks/list.html`, `todo/tests.py`.

---

## Task 5 — Export Tasks to CSV
**Priority:** Medium · **Status:** 🔲 To Do

Let the user download all tasks (or the currently filtered set) as a CSV file.

**Acceptance criteria**
- New URL `/tasks/export/` → `task_export` view.
- Returns `text/csv` with headers: `title, description, priority, due_date, completed, completed_at, created_at`.
- Respects the same filters as Task 3 when query params are present.
- "Export CSV" button on the task-list page.
- At least 2 unit tests (headers present, row count matches task count).

**Files touched:** `todo/views.py`, `todo/urls.py`, `templates/tasks/list.html`, `todo/tests.py`.

---

## Task 6 — Dark Mode Toggle
**Priority:** Low · **Status:** 🔲 To Do

Add a light/dark theme toggle that persists across sessions.

**Acceptance criteria**
- Toggle button in the navbar (sun/moon icon).
- Theme stored in `localStorage` and applied on page load.
- CSS variables for colors; `data-theme="dark"` attribute on `<html>`.
- No backend change required — pure front-end task.
- Manual QA checklist (all pages render correctly in both themes).

**Files touched:** `templates/base.html`, `static/css/style.css` *(new or extend)*.

---

## Summary

| # | Task | Priority | Est. effort |
|---|------|----------|-------------|
| 1 | Django Forms Hardening | High | ~1.5 h |
| 2 | Categories / Tags | High | ~2 h |
| 3 | Search & Filter | High | ~1.5 h |
| 4 | Overdue Indicator | Medium | ~1 h |
| 5 | CSV Export | Medium | ~1 h |
| 6 | Dark Mode Toggle | Low | ~1 h |

**Total estimated effort:** ~8 hours