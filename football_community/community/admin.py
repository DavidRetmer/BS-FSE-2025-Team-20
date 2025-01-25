from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event, Rating, Post, Comment

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'skill_level', 'date_joined', 'is_active')
    list_filter = ('skill_level', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Football Profile', {'fields': ('skill_level', 'location_latitude', 'location_longitude',
                                       'availability_days', 'availability_time_slots', 'bio')}),
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'datetime', 'location', 'max_players', 'is_active')
    list_filter = ('is_active', 'skill_level_filter', 'datetime')
    search_fields = ('title', 'description', 'location')
    raw_id_fields = ('organizer', 'participants')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    raw_id_fields = ('user', 'event')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
    raw_id_fields = ('author', 'post')
