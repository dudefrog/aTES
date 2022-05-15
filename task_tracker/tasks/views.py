import random

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from .forms import CreateTaskForm
from .models import Task
from .services import pick_random_user, shuffle_tasks
from task_tracker import events
from task_tracker.events import validate_and_publish
from users.models import User


def index_view(request: HttpRequest):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    form = CreateTaskForm()

    # --- shuffle tasks ---
    if (
        request.method == "POST"
        and request.POST.get("_action") == "shuffle-tasks"
        and request.user.role == "manager"
    ):
        shuffle_tasks()

    elif request.method == "POST":
        # --- close task ---
        if task_id := request.POST.get("task_id_to_complete"):
            task = Task.objects.get(id=int(task_id))
            task.is_closed = True
            task.save()
            validate_and_publish(events.TaskClosed_v1, task)
            form = CreateTaskForm()
        # --- add task ---
        else:
            form = CreateTaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=True)
                validate_and_publish(events.TaskAdded_v1, task)
                task.assignee = pick_random_user()
                task.save()
                validate_and_publish(events.TaskAssigned_v1, task)

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
