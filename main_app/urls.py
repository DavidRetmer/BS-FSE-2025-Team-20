from django.urls import path
from . import views
from .views import map_view
urlpatterns = [   
     path('',views.index,name = 'home'),
     path('about/',views.about, name='about'),
     path('join/',views.join, name='join'),
     path('contact/',views.contact, name='contact'),
     path('map/',map_view.as_view(), name='map'),
    ]
