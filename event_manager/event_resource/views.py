from django.shortcuts import render, get_object_or_404, redirect
from .models import Resource
from .forms import ResourceForm

def add_resource(request):
    if request.method == "POST":
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success_url')
    else:
        form = ResourceForm()
    return render(request, 'resource/add_resource.html', {'form': form})


def resource_list(request):
    query = request.GET.get('q')
    if query:
        resources = Resource.objects.filter(name__icontains=query)
    else:
        resources = Resource.objects.all()
    return render(request, 'resource/resource_list.html', {'resources': resources})

def edit_resource(request, id):
    resource = get_object_or_404(Resource, pk=id)
    if request.method == "POST":
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('event_resource:resource_list')  # Вернуться к списку ресурсов
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resource/edit_resource.html', {'form': form})