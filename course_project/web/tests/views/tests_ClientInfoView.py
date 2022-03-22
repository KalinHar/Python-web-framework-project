from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from course_project.web.models import Client


class ClientInfoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='aw3edcvb')
        self.web_client = Client.objects.create(names='Pepo Petrov',
                              phone='123456789',
                              old=0,
                              new=0,
                              username=User.objects.get(username='testuser'))

    def test_client_info_template_and_context(self):
        permission = Permission.objects.get(codename='view_client')
        self.user.user_permissions.add(permission)

        self.client.login(username='testuser', password='aw3edcvb')
        response = self.client.get(reverse('client details', kwargs={'pk': self.web_client.pk}))

        self.assertTemplateUsed(response, 'client-details.html')
        self.assertEqual(response.context['announce_count'], 0)
        self.assertEqual(response.context['labels'], '0')
        self.assertEqual(response.context['data'], '0')
        self.assertEqual(response.context['data_color'], '0')
        self.assertEqual(response.context['object'], self.web_client)


