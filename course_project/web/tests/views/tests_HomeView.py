from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_get__expect_correct_template(self):
        response = self.client.get(reverse('home'))

        self.assertTemplateUsed(response, 'home.html')

