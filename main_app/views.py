from django.conf import settings

from django.http import HttpResponse

from django.views import View

from .models import Messeges

from django.shortcuts import render, redirect

from .forms import SendMailForm

from .forms import ContactForm

class map_view(View):
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
        return render(request,'contact.html',{'form': ContactForm()})
    else:
        Messeges.objects.create(title=request.POST['title'], description=request.POST['description'])
        return redirect('')
    