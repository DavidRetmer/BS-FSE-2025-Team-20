from django.test import TestCase
from django.urls import reverse

class TemplateViewTests(TestCase):
    def test_base_template(self):
        response = self.client.get(reverse('home'))  # Asegúrate de que 'home' es el nombre de la URL para la vista que usa base.html
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, '<link rel="stylesheet" href="{% static \'styles/main.css\' %}">')

    def test_main_css(self):
        response = self.client.get(reverse('home'))  # Asegúrate de que 'home' es el nombre de la URL para la vista que usa base.html
        self.assertContains(response, '/* Barra de navegación */')
        self.assertContains(response, '.navbar {')