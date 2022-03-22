from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase
from django.urls import reverse

from course_project.web.models import Client, Taxes


class IndicationsListViewTests(TestCase):

    def setUp(self):
        User.objects.create_user(username='testuser', password='aw3edcvb')
        self.user = User.objects.all().first()
        # self.group = Group(name='Clients')
        # self.group.save()

        Client.objects.create(names='Pepo Petrov',
                              phone='123456789',
                              old=0,
                              new=0,
                              username=User.objects.get(username='testuser'))
        self.web_client = Client.objects.all()

        Taxes.objects.create(price=0.5, tax=10)

    def test_get__auth_user__expect_correct_template_context(self):
        # self.user.groups.add(self.group)
        # permission = Permission.objects.get(name='Can view client')
        permission = Permission.objects.get(codename='view_client')
        self.user.user_permissions.add(permission)

        self.client.login(username='testuser', password='aw3edcvb')
        response = self.client.get(reverse('indications'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'indications.html')

        self.assertEquals(response.context['price'], 0.5)
        self.assertEquals(response.context['tax'], 10)
        self.assertEquals(response.context['object_list'][0], self.web_client[0])

    def test_get__not_auth_user__expect_fail(self):
        self.client.login(username='testuser', password='aw3edcvb')
        response = self.client.get(reverse('indications'))

        self.assertEqual(response.status_code, 403)
        self.assertRaises(AssertionError)


