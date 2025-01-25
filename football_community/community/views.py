from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from .models import User, Event, Rating, Post, Comment, Message, EventAnnouncement, EventComment
from .forms import (
    UserRegistrationForm, UserProfileForm, EventForm,
    RatingForm, PostForm, CommentForm, MessageForm
)
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from django.core.mail import send_mail
from django.conf import settings

def unread_messages_processor(request):
    """Context processor to add unread messages count to all templates"""
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_messages_count': unread_count}
    return {'unread_messages_count': 0}

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('community:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'community/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('community:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'profile_user': request.user,
        'organized_events': request.user.organized_events.all()[:5],
        'participated_events': request.user.participated_events.all()[:5],
    }
    return render(request, 'community/profile.html', context)

@login_required
def event_list(request):
    events = Event.objects.filter(is_active=True, datetime__gte=timezone.now())
    
    # Filter by skill level
    skill_level = request.GET.get('skill_level')
    if skill_level:
        events = events.filter(skill_level_filter=skill_level)
    
    # Filter by distance if location is provided
    if request.user.location_latitude and request.user.location_longitude:
        max_distance = float(request.GET.get('distance', 10))  # Default 10km
        nearby_events = []
        
        for event in events:
            distance = calculate_distance(
                request.user.location_latitude,
                request.user.location_longitude,
                event.location_latitude,
                event.location_longitude
            )
            if distance <= max_distance:
                event.distance = round(distance, 1)
                nearby_events.append(event)
        
        events = sorted(nearby_events, key=lambda x: x.distance)
    
    paginator = Paginator(events, 10)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    
    return render(request, 'community/event_list.html', {'events': events})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('community:event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'community/event_form.html', {'form': form})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_rating = Rating.objects.filter(event=event, user=request.user).first()
    
    if request.method == 'POST':
        if 'join' in request.POST:
            event.participants.add(request.user)
            messages.success(request, 'You have joined the event!')
        elif 'leave' in request.POST:
            event.participants.remove(request.user)
            messages.success(request, 'You have left the event!')
        elif 'comment' in request.POST:
            comment_content = request.POST.get('content')
            if comment_content:
                EventComment.objects.create(
                    event=event,
                    author=request.user,
                    content=comment_content
                )
                messages.success(request, 'Comment added successfully!')
            else:
                messages.error(request, 'Comment cannot be empty.')
        return redirect('community:event_detail', event_id=event.id)
    
    context = {
        'event': event,
        'user_rating': user_rating,
        'avg_rating': event.ratings.aggregate(Avg('score'))['score__avg'],
        'participant_count': event.participants.count(),
        'is_participant': request.user in event.participants.all(),
        'now': timezone.now(),
        'event_announcements': event.announcements.all(),
        'event_comments': event.comments.select_related('author').all(),
    }
    return render(request, 'community/event_detail.html', context)

@login_required
def event_announcement(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Only allow the event organizer to post announcements
    if request.user != event.organizer:
        messages.error(request, 'Only the event organizer can post announcements.')
        return redirect('community:event_detail', event_id=event.id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            EventAnnouncement.objects.create(
                event=event,
                content=content
            )
            messages.success(request, 'Announcement posted successfully!')
        else:
            messages.error(request, 'Announcement content cannot be empty.')
    
    return redirect('community:event_detail', event_id=event.id)

@login_required
def rate_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.event = event
            rating.save()
            messages.success(request, 'Rating submitted successfully!')
            return redirect('community:event_detail', event_id=event.id)
    else:
        form = RatingForm()
    return render(request, 'community/rating_form.html', {'form': form, 'event': event})

@login_required
def post_list(request):
    posts = Post.objects.annotate(comment_count=Count('comments')).order_by('-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'community/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('community:post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'community/post_form.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('author')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('community:post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'community/post_detail.html', context)

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author
    if request.user != post.author:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('community:post_detail', post_id=post.id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('community:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'community/post_form.html', {'form': form})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author
    if request.user != post.author:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('community:post_detail', post_id=post.id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('community:post_list')
    
    return redirect('community:post_detail', post_id=post.id)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers using the Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return distance

def about(request):
    return render(request, 'community/about.html')

def home(request):
    return render(request, 'community/home.html')

@login_required
def inbox(request):
    """View for displaying user's messages"""
    received_messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    
    # Get unread messages count
    unread_count = received_messages.filter(is_read=False).count()
    
    # Mark messages as read when viewing inbox
    if request.GET.get('mark_read'):
        received_messages.filter(is_read=False).update(is_read=True)
    
    context = {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'unread_messages_count': unread_count,
    }
    return render(request, 'community/inbox.html', context)

@login_required
def send_message(request, recipient_id):
    """View for sending a message to another user"""
    recipient = get_object_or_404(User, id=recipient_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('community:inbox')
    else:
        form = MessageForm()
    
    context = {
        'form': form,
        'recipient': recipient,
    }
    return render(request, 'community/message_form.html', context)

@login_required
def message_detail(request, message_id):
    """View for displaying a single message"""
    message = get_object_or_404(
        Message,
        Q(recipient=request.user) | Q(sender=request.user),
        id=message_id
    )
    
    # Mark message as read if user is recipient
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save()
    
    context = {
        'message': message,
    }
    return render(request, 'community/message_detail.html', context)

def is_moderator(user):
    return user.is_admin_or_moderator()

@login_required
@user_passes_test(is_moderator)
def admin_dashboard(request):
    """Admin dashboard view"""
    # Get statistics for the dashboard
    total_users = User.objects.count()
    total_events = Event.objects.count()
    total_posts = Post.objects.count()
    
    # Recent activity
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_events = Event.objects.order_by('-created_at')[:5]
    recent_posts = Post.objects.order_by('-created_at')[:5]
    
    # Activity in the last 7 days
    last_week = timezone.now() - timedelta(days=7)
    new_users_count = User.objects.filter(date_joined__gte=last_week).count()
    new_events_count = Event.objects.filter(created_at__gte=last_week).count()
    new_posts_count = Post.objects.filter(created_at__gte=last_week).count()
    
    context = {
        'total_users': total_users,
        'total_events': total_events,
        'total_posts': total_posts,
        'recent_users': recent_users,
        'recent_events': recent_events,
        'recent_posts': recent_posts,
        'new_users_count': new_users_count,
        'new_events_count': new_events_count,
        'new_posts_count': new_posts_count,
    }
    return render(request, 'community/admin/dashboard.html', context)

@login_required
@user_passes_test(is_moderator)
def admin_users(request):
    """User management view"""
    users = User.objects.all().order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Handle user actions
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = get_object_or_404(User, id=user_id)
        
        if action == 'toggle_moderator':
            if request.user.is_superuser:  # Only superusers can manage moderators
                user.is_moderator = not user.is_moderator
                user.save()
                messages.success(request, f'Updated moderator status for {user.username}')
            else:
                messages.error(request, 'Only superusers can manage moderators')
        
        elif action == 'toggle_active':
            user.is_active = not user.is_active
            user.save()
            messages.success(request, f'Updated active status for {user.username}')
    
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    return render(request, 'community/admin/users.html', {'users': users})

@login_required
@user_passes_test(is_moderator)
def admin_events(request):
    """Event management view"""
    events = Event.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(organizer__username__icontains=search_query)
        )
    
    # Handle event actions
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        action = request.POST.get('action')
        event = get_object_or_404(Event, id=event_id)
        
        if action == 'toggle_active':
            event.is_active = not event.is_active
            event.save()
            messages.success(request, f'Updated status for event: {event.title}')
        
        elif action == 'delete':
            event.delete()
            messages.success(request, 'Event deleted successfully')
    
    paginator = Paginator(events, 20)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    
    return render(request, 'community/admin/events.html', {'events': events})

@login_required
@user_passes_test(is_moderator)
def admin_posts(request):
    """Post management view"""
    posts = Post.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Handle post actions
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        post = get_object_or_404(Post, id=post_id)
        
        if action == 'delete':
            post.delete()
            messages.success(request, 'Post deleted successfully')
    
    paginator = Paginator(posts, 20)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'community/admin/posts.html', {'posts': posts})

@login_required
@user_passes_test(is_moderator)
def admin_reports(request):
    """View for handling reported content"""
    # Get all reported content
    reported_posts = Post.objects.filter(is_reported=True).order_by('-reported_at')
    reported_events = Event.objects.filter(is_reported=True).order_by('-reported_at')
    reported_users = User.objects.filter(is_reported=True).order_by('-reported_at')
    
    # Handle report actions
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        content_id = request.POST.get('content_id')
        action = request.POST.get('action')
        
        if content_type == 'post':
            content = get_object_or_404(Post, id=content_id)
        elif content_type == 'event':
            content = get_object_or_404(Event, id=content_id)
        elif content_type == 'user':
            content = get_object_or_404(User, id=content_id)
        
        if action == 'dismiss':
            content.is_reported = False
            content.save()
            messages.success(request, 'Report dismissed successfully')
        elif action == 'delete':
            content.delete()
            messages.success(request, 'Content deleted successfully')
    
    context = {
        'reported_posts': reported_posts,
        'reported_events': reported_events,
        'reported_users': reported_users,
    }
    return render(request, 'community/admin/reports.html', context)

@login_required
def report_post(request, post_id):
    """View for reporting a post"""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        reason = request.POST.get('reason')
        
        post.is_reported = True
        post.reported_at = timezone.now()
        post.report_reason = reason
        post.save()
        
        messages.success(request, 'Post has been reported to moderators.')
        return redirect('community:post_detail', post_id=post_id)
    
    return redirect('community:post_detail', post_id=post_id)

@login_required
def report_event(request, event_id):
    """View for reporting an event"""
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        reason = request.POST.get('reason')
        
        event.is_reported = True
        event.reported_at = timezone.now()
        event.report_reason = reason
        event.save()
        
        messages.success(request, 'Event has been reported to moderators.')
        return redirect('community:event_detail', event_id=event_id)
    
    return redirect('community:event_detail', event_id=event_id)

@login_required
def report_user(request, user_id):
    """View for reporting a user"""
    if request.method == 'POST':
        reported_user = get_object_or_404(User, id=user_id)
        reason = request.POST.get('reason')
        
        # Don't allow reporting moderators or admins
        if reported_user.is_admin_or_moderator():
            messages.error(request, 'You cannot report moderators or administrators.')
            return redirect('community:profile')
        
        reported_user.is_reported = True
        reported_user.reported_at = timezone.now()
        reported_user.report_reason = reason
        reported_user.save()
        
        messages.success(request, 'User has been reported to moderators.')
        return redirect('community:profile')
    
    return redirect('community:profile')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Create a post to track the contact form submission
        contact_post = Post.objects.create(
            title=f'Contact Form: {subject}',
            content=f'From: {name}\nEmail: {email}\n\nMessage:\n{message}',
            author=request.user if request.user.is_authenticated else User.objects.get(is_superuser=True),
            is_reported=True,  # Mark as reported so it shows up in reports
            reported_at=timezone.now(),
            report_reason='Contact Form Submission'
        )
        
        # Compose and send email
        email_subject = f'Contact Form: {subject}'
        email_message = f'From: {name}\nEmail: {email}\n\nMessage:\n{message}'
        
        try:
            # Send email
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
        
        return redirect('community:about')
    
    return redirect('community:about')
