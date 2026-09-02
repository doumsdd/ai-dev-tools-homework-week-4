from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task


def home(request):
    """Dashboard - overview of all tasks."""
    tasks = Task.objects.all()
    pending_tasks = tasks.filter(completed=False)
    completed_tasks = tasks.filter(completed=True)

    context = {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'home.html', context)


# Task views
def task_list(request):
    """List all tasks."""
    tasks = Task.objects.all()
    return render(request, 'tasks/list.html', {'tasks': tasks})


def task_add(request):
    """Add a new task."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')

        if title:
            task = Task(
                title=title,
                description=description,
                priority=priority or 'medium',
            )
            if due_date:
                task.due_date = due_date
            task.save()
            return redirect('task_list')

    context = {
        'priorities': Task.PRIORITY_CHOICES,
    }
    return render(request, 'tasks/add.html', context)


def task_edit(request, pk):
    """Edit an existing task."""
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.priority = request.POST.get('priority', task.priority)

        due_date = request.POST.get('due_date')
        if due_date:
            task.due_date = due_date
        else:
            task.due_date = None

        task.save()
        return redirect('task_list')

    context = {
        'task': task,
        'priorities': Task.PRIORITY_CHOICES,
    }
    return render(request, 'tasks/edit.html', context)


def task_delete(request, pk):
    """Delete a task."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/delete.html', {'task': task})


def task_complete(request, pk):
    """Mark a task as completed."""
    task = get_object_or_404(Task, pk=pk)
    task.completed = True
    task.completed_at = timezone.now()
    task.save()
    return redirect('home')