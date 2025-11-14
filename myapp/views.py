from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from .models import Project, Task
from django.http import HttpResponse
from .forms import CreateNewTask, CreateNewProject
from django.conf import settings

def index(request):
    title = 'Examen de DJango'
    return render(request, 'index.html', {
        'title': title
    })

def projects(request):
    projects = list(Project.objects.values())
    return render(request, 'projects/projects.html', {
        'projects': projects
    })

class TaskListView(ListView):
    model = Task
    template_name = "tasks/tasks.html"
    context_object_name = "tasks"

def create_task(request):
    if request.method == 'GET':
        projects = list(Project.objects.values())
        return render(request, 'tasks/create_task.html', {
            'form': CreateNewTask(),
            'projects': projects
        })
    else:
        Task.objects.create(
            title=request.POST['title'], description=request.POST['description'], project_id=request.POST['project_id'])
        title = request.POST['title']
        description = request.POST['description']
        project_id = request.POST['project_id']
        # Guardar en Mongo
        settings.MONGO_TASKS.insert_one({
            "Title": title,
            "Description": description,
            "Done": False,
            "project_id": project_id
        })
        return redirect('tasks')
    
def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject()
        })
    else:
        Project.objects.create(name=request.POST["name"])
        name = request.POST["name"]
        settings.MONGO_PROJECTS.insert_one({
            "name": name
        })
        return redirect('projects')

def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=id)
    return render(request, 'projects/detail.html', {
        'project': project,
        'tasks': tasks
    })