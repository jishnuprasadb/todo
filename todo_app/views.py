from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import TodoForm
from . models import Task
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView


# Create your views here.
def home(request):
    task1 = Task.objects.all()
    if request.method=='POST':
        name=request.POST['task']
        priority=request.POST['priority']
        date=request.POST['date']
        task=Task(name=name,priority=priority,date=date)
        task.save()
    return render(request,'home.html',{'task':task1})


def delete(request,id):
    task=Task.objects.get(id=id)
    if request.method=='POST':
        task.delete()
        return redirect('/')

    return render(request,'delete.html')


def update(request,id):
    task=Task.objects.get(id=id)
    form=TodoForm(request.POST or None,instance=task)
    if form.is_valid():
        form.save()
        return redirect(('/'))
    return render(request,'edit.html',{'form':form})



class TaskListView(ListView):
    model=Task
    template_name='home.html'
    context_object_name='task'


class TskDetailView(DetailView):
    model=Task
    template_name='details.html'
    context_object_name='task'

class TaskUpdateView(UpdateView):
    model = Task
    template_name='update.html'
    context_object_name='task'
    fields=('name','date','priority')

    def get_success_url(self):
        return reverse_lazy('cbvdetails',kwargs={'pk':self.object.id})


class TaskDeleteView(DeleteView):
    model = Task
    template_name='delete.html'
    success_url = reverse_lazy('cbvhome')
