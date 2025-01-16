
from django.http import HttpResponse

from django.shortcuts import render

from .forms import SendMailForm

from .forms import TaskForm

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def join(request):
    return render(request,'join.html', {'form': SendMailForm()})

def contact(request):
    return render(request,'contact.html',{'form': TaskForm()})