from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from course_project.web.models import Client, Taxes, Master


class PaymentsViewTest(TestCase):
    def create_user_and_client(self, username, password):
        user = User.objects.create_user(username=username, password=password)
        web_client = Client.objects.create(names='client - ' + username,
                              phone='123456789',
                              old=0,
                              new=10,
                              username=User.objects.get(username=username))
        return user, web_client

    def get_taxes(self):
        Taxes.objects.create(price=0.5, tax=5)
        return Taxes.objects.all()

    def setUp(self):
        permission = Permission.objects.get(codename='change_taxes')
        self.user, self.web_client = self.create_user_and_client('casher', 'aw3edcvb')
        self.user.user_permissions.add(permission)
        self.client.login(username='casher', password='aw3edcvb')
        Master.objects.create(old=100, new=300)

        self.web_clients = Client.objects.all()
        self.taxes = self.get_taxes()

    def test_payments_template_and_context(self):
        response = self.client.get(reverse('payments'))

        self.assertTemplateUsed(response, 'payments/payments.html')
        self.assertEqual(response.context['m_units'], 200)
        self.assertEqual(response.context['m_cost'], 100)
        self.assertEqual(response.context['price'], 0.5)
        self.assertEqual(response.context['tax'], 5)
        self.assertEqual(response.context['debit'], 0)
        self.assertEqual(response.context['total'], 10)
        self.assertEqual(response.context['cl_units'], 10)

    def test_pay_to_client(self):
        response = self.client.get(reverse('pay to', kwargs={'pk': self.web_client.pk}))
        self.web_client.refresh_from_db()

        self.assertTrue(self.web_client.paid)
        self.assertRedirects(response, '/payments/')

    def test_get_edit_taxes_and_context(self):
        response = self.client.get(reverse('taxes', kwargs={'pk': self.taxes[0].pk}))

        self.assertEqual(response.context['paid_clients'], 0)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_taxes(self):
        response = self.client.post(reverse('taxes', kwargs={'pk': self.taxes[0].pk}), data={'price':0.2, 'tax':2})
        self.taxes[0].refresh_from_db()

        self.assertEqual(self.taxes[0].price, 0.2)
        self.assertRedirects(response, '/payments/')

    def test_get_edit_client_and_context(self):
        response = self.client.get(reverse('edit client', kwargs={'pk': self.web_client.pk}))

        self.assertEqual(response.context['object'], self.web_client)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_client(self):
        response = self.client.post(reverse('edit client',
                                            kwargs={'pk': self.web_client.pk}),
                                            data={'names':'changed name',
                                                  'phone':'123456789',
                                                  'old':0,
                                                  'new':10,
                                                  'paid':True,
                                                  'username':self.user})
        self.web_client.refresh_from_db()

        self.assertEqual(self.web_client.names, 'changed name')
        self.assertEqual(self.web_client.paid, True)
        self.assertRedirects(response, '/payments/')
