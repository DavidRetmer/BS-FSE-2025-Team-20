from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.utils import timezone
from multiselectfield import MultiSelectField

class User(AbstractUser):
    # User roles and permissions
    is_moderator = models.BooleanField(default=False)
    can_moderate_content = models.BooleanField(default=False)
    can_manage_events = models.BooleanField(default=False)
    can_ban_users = models.BooleanField(default=False)
    
    # Reporting fields
    is_reported = models.BooleanField(default=False)
    reported_at = models.DateTimeField(null=True, blank=True)
    report_reason = models.TextField(blank=True)

    # Profile fields
    bio = models.TextField(max_length=500, blank=True)
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('professional', 'Professional')
        ],
        default='beginner'
    )
    
    # Location fields
    location_latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text="User's latitude coordinate"
    )
    location_longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text="User's longitude coordinate"
    )
    location_updated_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When the location was last updated"
    )

    # Availability fields
    availability_days = MultiSelectField(
        choices=[
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday')
        ],
        max_length=100,
        blank=True
    )
    availability_time_slots = MultiSelectField(
        choices=[
            ('morning', 'Morning (6 AM - 12 PM)'),
            ('afternoon', 'Afternoon (12 PM - 5 PM)'),
            ('evening', 'Evening (5 PM - 10 PM)')
        ],
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        permissions = [
            ("can_moderate_content", "Can moderate community content"),
            ("can_manage_events", "Can manage all events"),
            ("can_ban_users", "Can ban users from the community"),
        ]

    def is_admin_or_moderator(self):
        return self.is_staff or self.is_moderator

    def save(self, *args, **kwargs):
        if self.location_latitude or self.location_longitude:
            self.location_updated_at = timezone.now()
        super().save(*args, **kwargs)

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    max_players = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(22)])
    skill_level_filter = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('professional', 'Professional')
        ],
        null=True,
        blank=True
    )
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    participants = models.ManyToManyField(User, related_name='participated_events', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Reporting fields
    is_reported = models.BooleanField(default=False)
    reported_at = models.DateTimeField(null=True, blank=True)
    report_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'events'
        ordering = ['-datetime']

class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ratings'
        unique_together = ['user', 'event']  # One rating per user per event

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Reporting fields
    is_reported = models.BooleanField(default=False)
    reported_at = models.DateTimeField(null=True, blank=True)
    report_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['created_at']

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'

class EventAnnouncement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='announcements')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'event_announcements'
        ordering = ['-created_at']

    def __str__(self):
        return f'Announcement for {self.event.title}'

class EventComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'event_comments'
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.event.title}'
