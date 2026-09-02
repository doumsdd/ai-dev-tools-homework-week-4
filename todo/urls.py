from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path("", views.home, name="home"),

    # Task URLs
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/add/", views.task_add, name="task_add"),
    path("tasks/<int:pk>/edit/", views.task_edit, name="task_edit"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("tasks/<int:pk>/complete/", views.task_complete, name="task_complete"),
]