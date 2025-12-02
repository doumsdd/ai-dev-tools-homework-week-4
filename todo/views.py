from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Todo

def home(request):
    todos = Todo.objects.all()
    return render(request, "home.html", {"todos": todos})
