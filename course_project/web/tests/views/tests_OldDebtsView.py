from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from course_project.web.models import Client, OldDebts, Taxes, Master


class OldDebtsViewTests(TestCase):
    def create_user_and_client(self, username, password):
        user = User.objects.create_user(username=username, password=password)
        web_client = Client.objects.create(names='client - ' + username,
                                           phone='123456789',
                                           old=0,
                                           new=10,
                                           old_debts=1,
                                           username=User.objects.get(username=username))
        return user, web_client

    def setUp(self):
        self.user, self.web_client = self.create_user_and_client('casher', 'aw3edcvb')
        self.client.login(username='casher', password='aw3edcvb')
        self.old_debt = OldDebts.objects.create(client=self.web_client,
                                                debts=5.55,
                                                indications='xyz')

        self.web_clients = Client.objects.all()
        Taxes.objects.create(price=0.5, tax=5)
        Master.objects.create(old=100, new=300)

    def test_old_debts_template_and_context(self):
        permission = Permission.objects.get(codename='change_taxes')
        self.user.user_permissions.add(permission)
        response = self.client.get(reverse('old debts'))

        self.assertEqual(response.context['object_list'][0], self.old_debt)
        self.assertTrue(response.context['pay_btn'])
        self.assertTemplateUsed(response, 'payments/old-debts.html')

    def test_clear_debts(self):
        permission = Permission.objects.get(codename='change_taxes')
        self.user.user_permissions.add(permission)
        response = self.client.get(reverse('clear debt', kwargs={'pk': self.old_debt.pk}))
        self.web_client.refresh_from_db()

        self.assertEqual(self.web_client.old_debts, 0)
        self.assertEqual(OldDebts.objects.count(), 0)
        self.assertRedirects(response, '/payments/')

    def test_client_debts_template_and_context(self):
        permission = Permission.objects.get(codename='view_client')
        self.user.user_permissions.add(permission)
        response = self.client.get(reverse('client debts', kwargs={'pk': self.web_client.pk}))

        self.assertEqual(response.context['object_list'][0], self.old_debt)
        self.assertFalse(response.context['pay_btn'])
        self.assertTemplateUsed(response, 'payments/old-debts.html')
