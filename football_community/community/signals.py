from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, Rating, User

@receiver(post_save, sender=Event)
def notify_event_creation(sender, instance, created, **kwargs):
    """Send notification when a new event is created"""
    if created:
        # In a real application, you would want to use a task queue like Celery for this
        subject = f'New Football Event: {instance.title}'
        message = f'''
        A new football event has been created!
        
        Title: {instance.title}
        Date: {instance.datetime}
        Location: {instance.location}
        Organizer: {instance.organizer.username}
        Max Players: {instance.max_players}
        
        Join now to secure your spot!
        '''
        # In production, you would want to filter users based on location and preferences
        recipients = User.objects.filter(is_active=True).values_list('email', flat=True)
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(recipients),
            fail_silently=True,
        )

@receiver(m2m_changed, sender=Event.participants.through)
def notify_participant_change(sender, instance, action, pk_set, **kwargs):
    """Send notification when participants join or leave an event"""
    if action == "post_add":
        # Notify organizer about new participants
        new_participants = User.objects.filter(pk__in=pk_set)
        subject = f'New Participants in {instance.title}'
        message = f'''
        New players have joined your event!
        
        Event: {instance.title}
        New Participants: {", ".join(user.username for user in new_participants)}
        Total Participants: {instance.participants.count()}/{instance.max_players}
        '''
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.organizer.email],
            fail_silently=True,
        )

@receiver(post_save, sender=Rating)
def notify_event_rating(sender, instance, created, **kwargs):
    """Notify event organizer about new ratings"""
    if created:
        subject = f'New Rating for {instance.event.title}'
        message = f'''
        Your event received a new rating!
        
        Event: {instance.event.title}
        Rating: {instance.score}/5
        Feedback: {instance.feedback}
        '''
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.event.organizer.email],
            fail_silently=True,
        ) 