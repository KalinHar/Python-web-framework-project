from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from course_project.web.models import Client, Archive, Taxes
from django.core import serializers


class ClientInfoViewTest(TestCase):

    def create_user_and_client(self, username, password):
        user = User.objects.create_user(username=username, password=password)
        web_client = Client.objects.create(names='client - ' + username,
                              phone='123456789',
                              old=0,
                              new=7,
                              username=User.objects.get(username=username))
        return user, web_client

    def add_to_archive(self, clients, taxes):
        data = serializers.serialize('json', clients)
        taxes = serializers.serialize('json', taxes)
        Archive.objects.create(data=data, taxes=taxes)
        Client.objects.all().update(reported=False)

    def get_taxes(self):
        Taxes.objects.create(price=0.5, tax=5)
        return Taxes.objects.all()

    def test_client_info_template_and_context(self):
        permission = Permission.objects.get(codename='view_client')
        user, web_client = self.create_user_and_client('testuser', 'aw3edcvb')
        user.user_permissions.add(permission)
        self.client.login(username='testuser', password='aw3edcvb')

        clients = Client.objects.all()
        taxes = self.get_taxes()
        self.add_to_archive(list(clients), list(taxes))

        response = self.client.get(reverse('client details', kwargs={'pk': web_client.pk}))

        self.assertTemplateUsed(response, 'indications-info/client-details.html')
        self.assertEqual(response.context['announce_count'], 0)
        self.assertIsNotNone(response.context['labels'])
        self.assertEqual(response.context['data'], '[7]')
        self.assertIsNotNone(response.context['data_color'])
        self.assertEqual(response.context['object'], web_client)


