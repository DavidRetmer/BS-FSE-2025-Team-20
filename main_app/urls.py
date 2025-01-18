from django.urls import path
from . import views
from .views import MapView
urlpatterns = [   
     path('',views.index,name = 'home'),
     path('about/',views.about, name='about'),
     path('join/',views.join, name='join'),
     path('contact/',views.contact, name='contact'),
     path('map/',MapView.as_view(), name='map'),
     path('register/',views.registerPage,name='register'),
     path('login/',views.loginPage,name='login')
    ]
