from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'community'

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    
    # Static Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='community/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='community:login'
    ), name='logout'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    
    # Event URLs
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<uuid:event_id>/', views.event_detail, name='event_detail'),
    path('events/<uuid:event_id>/rate/', views.rate_event, name='rate_event'),
    path('events/<uuid:event_id>/announcement/', views.event_announcement, name='event_announcement'),
    
    # Community URLs
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<uuid:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<uuid:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<uuid:post_id>/delete/', views.post_delete, name='post_delete'),

    # Messaging URLs
    path('inbox/', views.inbox, name='inbox'),
    path('messages/send/<int:recipient_id>/', views.send_message, name='send_message'),
    path('messages/<uuid:message_id>/', views.message_detail, name='message_detail'),

    # Admin Panel URLs
    path('manage/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage/users/', views.admin_users, name='admin_users'),
    path('manage/events/', views.admin_events, name='admin_events'),
    path('manage/posts/', views.admin_posts, name='admin_posts'),
    path('manage/reports/', views.admin_reports, name='admin_reports'),
    
    # Report URLs
    path('report/post/<uuid:post_id>/', views.report_post, name='report_post'),
    path('report/event/<uuid:event_id>/', views.report_event, name='report_event'),
    path('report/user/<uuid:user_id>/', views.report_user, name='report_user'),
] 