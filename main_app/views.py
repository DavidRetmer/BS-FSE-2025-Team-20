from django.conf import settings
from django.http import HttpResponse
from django.views import View
from .models import Messages
from django.shortcuts import render, redirect
from .forms import SendMailForm
from .forms import ContactForm,CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib import messages


def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account was created for {user}')
            return redirect('login')

    context = {'form' : form}
    return render(request,'accounts/register.html',context)

def loginPage(request):
    context = {}
    return render(request,'accounts/login.html',context)

class MapView(View):
    template_name = "map.html"

    def get(self, request):
        key = settings.GOOGLE_API_KEY
        context = {'key': key}
        return render(request, self.template_name,context)

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def join(request):
    return render(request,'join.html', {'form': SendMailForm()})

def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html', {'form': ContactForm()})
    else:
        Messages.objects.create(
            title=request.POST.get('title', ''), 
            description=request.POST.get('description', '')
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    