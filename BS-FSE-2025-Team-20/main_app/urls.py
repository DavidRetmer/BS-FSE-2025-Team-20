from django.urls import path
from . import views
from .views import MapView
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [   
     path('home/',views.index,name = 'home'),
     path('about/',views.about, name='about'),
     path('join/',views.join, name='join'),
     path('contact/',views.contact, name='contact'),
     path('register/',views.registerPage,name='register'),
     path('login/',views.loginPage,name='login'),
     path('welcome_admin/', views.welcome_admin, name='welcome_admin'),
     path('admin_login/', views.admin_login, name='admin_login'),
     path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
     path('events_view/', views.events_view, name='events_view'),
     path('events_map/', views.events_map, name='events_map'),
     path('rate_complaint/', views.rate_complaint, name='rate_complaint'),
     path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
path('events/',views.events,name='events'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('add_event/', views.add_event, name='add_event'),
     path('login_admin/', views.add_event, name='login_admin'),
path('welcome/', views.welcome, name='welcome'),
     path('welcome/', views.welcome, name='welcome'),
path('login/admin/', views.login_admin, name='login_admin'),
    # אם יש לך דף ברוך הבא לאדמין
    path('admin/welcome/', views.welcome_admin, name='welcome_admin'),
path('', views.index, name='index'),
]
