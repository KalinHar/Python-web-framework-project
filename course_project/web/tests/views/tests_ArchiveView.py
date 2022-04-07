from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from course_project.web.models import Client, Archive, Taxes
from django.core import serializers


class ArchiveViewTest(TestCase):
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

    def setUp(self):
        permission = Permission.objects.get(codename='view_client')
        user, self.web_client = self.create_user_and_client('testuser', 'aw3edcvb')
        user.user_permissions.add(permission)
        self.client.login(username='testuser', password='aw3edcvb')

        clients = Client.objects.all()
        taxes = self.get_taxes()
        self.add_to_archive(list(clients), list(taxes))
        self.arch = Archive.objects.first()

    def test_all_archive_template_and_context(self):
        response = self.client.get(reverse('all archive'))

        self.assertTemplateUsed(response, 'archive.html')
        self.assertFalse(response.context['only_one'])

    def test_one_archive_view_template_and_context(self):
        response = self.client.get(reverse('view archive', kwargs={'pk': self.arch.pk}))

        self.assertTemplateUsed(response, 'archive.html')
        self.assertTrue(response.context['only_one'])
        self.assertIsNotNone(response.context['from_date'])
        self.assertIsNotNone(response.context['clients'])
        self.assertIsNotNone(response.context['taxes'])

    def test_export_archive(self):
        response = self.client.get(reverse('download archive', kwargs={'pk': self.arch.pk}))
        self.assertIsNotNone(response.content)
