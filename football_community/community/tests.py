from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import User, Event, Post, Rating, Message
from datetime import timedelta
from django.contrib.auth import get_user_model
import uuid

# Create your tests here.

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_registration(self):
        response = self.client.post(reverse('community:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        self.assertEqual(response.status_code, 302)  # Expect redirect after successful registration
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_user_login(self):
        response = self.client.post(reverse('community:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)  # Expect redirect after successful login
        self.assertTrue('_auth_user_id' in self.client.session)

class EventTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_create_event(self):
        response = self.client.post(reverse('community:event_create'), {
            'title': 'Test Event',
            'description': 'Test Description',
            'location': 'Test Location',
            'datetime': timezone.now() + timezone.timedelta(days=1),
            'max_players': 10,
        })
        self.assertEqual(response.status_code, 302)  # Expect redirect after creation

class CommunityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = get_user_model().objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_messaging(self):
        response = self.client.post(
            reverse('community:send_message', args=[self.other_user.id]),
            {'content': 'Test message'}
        )
        self.assertEqual(response.status_code, 302)  # Expect redirect after sending message

    def test_create_post(self):
        response = self.client.post(reverse('community:post_create'), {
            'title': 'Test Post',
            'content': 'Test Content',
        })
        self.assertEqual(response.status_code, 302)  # Expect redirect after creation

    def test_profile_update(self):
        response = self.client.post(reverse('community:profile'), {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'bio': 'Test bio',
            'skill_level': 'intermediate',
        })
        self.assertEqual(response.status_code, 302)  # Expect redirect after update
