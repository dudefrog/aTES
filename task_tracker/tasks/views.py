import random

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from .forms import CreateTaskForm
from .models import Task
from task_tracker.async_messaging import TaskAdded, TaskAssigned, TaskClosed
from users.models import User


def pick_random_user() -> User:
    all_users = list(User.objects.exclude(username="admin").all())
    return random.choice(all_users)


# Create your views here.
def index_view(request: HttpRequest):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")

    if request.method == "POST":
        if task_id := request.POST.get("task_id_to_complete"):
            task = Task.objects.get(id=int(task_id))
            task.is_closed = True
            task.save()
            TaskClosed(task).send()
            form = CreateTaskForm()
        else:
            form = CreateTaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=True)
                TaskAdded(task).send()
                task.assignee = pick_random_user()
                TaskAssigned(task).send()
                task.save()

    elif request.method == "GET":
        form = CreateTaskForm()

    all_tasks = Task.objects.all()
    user_tasks = Task.objects.filter(assignee=request.user, is_closed=False).all()

    return render(
        request,
        "tasks/index.html",
        {
            "form": form,
            "tasks": all_tasks,
            "user_tasks": user_tasks,
        },
    )
