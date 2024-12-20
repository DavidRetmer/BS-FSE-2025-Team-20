from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Home page view
def home(request):
    return render(request, 'home.html')
