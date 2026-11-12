from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Project, Task
from .forms import ProjectForm, TaskForm

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created! Welcome to TaskFlow.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    projects = Project.objects.filter(owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, f'Project "{project.title}" created.')
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'tasks/dashboard.html', {'projects': projects, 'form': form})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    tasks = project.tasks.all()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, 'Task added.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/project_detail.html', {
        'project': project,
        'tasks': tasks,
        'form': form,
    })

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        project.delete()
        messages.info(request, 'Project deleted.')
        return redirect('dashboard')
    return render(request, 'tasks/confirm_delete.html', {'object': project, 'type': 'Project'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('project_detail', pk=task.project.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    project_pk = task.project.pk
    if request.method == 'POST':
        task.delete()
        messages.info(request, 'Task removed.')
        return redirect('project_detail', pk=project_pk)
    return render(request, 'tasks/confirm_delete.html', {'object': task, 'type': 'Task'})

@login_required
@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return JsonResponse({'id': task.id, 'is_completed': task.is_completed})
