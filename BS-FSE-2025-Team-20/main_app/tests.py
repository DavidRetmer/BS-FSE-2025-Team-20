from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import Client


class WelcomePageTests(TestCase):

    def setUp(self):
        """הכנת משתמשים ובחינה בסיסית"""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()

    def test_welcome_page_logged_in(self):
        """בדיקה אם המשתמש מחובר, הדף של 'welcome' נטען בהצלחה"""
        # נכנסים עם פרטי המשתמש
        self.client.login(username='testuser', password='12345')

        # גישה לדף ברוך הבא
        response = self.client.get(reverse('welcome'))

        # בדיקה אם הדף נטען בהצלחה (200)
        self.assertEqual(response.status_code, 200)

        # בדיקה אם שם המשתמש מוצג בדף
        self.assertContains(response, "Welcome, testuser!")

    def test_welcome_page_not_logged_in(self):
        """בדיקה אם המשתמש לא מחובר, הוא ינותב לדף ההתחברות"""
        # גישה לדף ברוך הבא בלי להתחבר
        response = self.client.get(reverse('welcome'))

        # בדיקה אם נעשה הפניה לדף ההתחברות (302)
        self.assertEqual(response.status_code, 302)

        # בדיקה אם ההפניה לדף ההתחברות
        self.assertRedirects(response, '/login/?next=/welcome/')
