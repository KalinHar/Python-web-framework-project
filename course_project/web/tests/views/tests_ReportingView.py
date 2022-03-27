from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from course_project.web.models import Client, Taxes, Master, Archive


class ReportingViewTest(TestCase):
    def create_user_and_client(self, username, password):
        user = User.objects.create_user(username=username, password=password)
        web_client = Client.objects.create(names='client - ' + username,
                              phone='123456789',
                              old=0,
                              new=10,
                              username=User.objects.get(username=username))
        return user, web_client

    def setUp(self):
        permission = Permission.objects.get(codename='add_archive')
        self.user, self.web_client = self.create_user_and_client('reporter', 'aw3edcvb')
        self.user.user_permissions.add(permission)
        self.client.login(username='reporter', password='aw3edcvb')
        self.master = Master.objects.create(old=100, new=300)
        Taxes.objects.create(price=0.5, tax=5)
        self.web_clients = Client.objects.all()

    def test_reporting_template_and_context_when_not_all_reported(self):
        response = self.client.get(reverse('reporting'))

        self.assertTemplateUsed(response, 'reporting/reporting.html')
        self.assertFalse(response.context['all_reported'])
        self.assertIsNotNone(response.context['object_list'])

    def test_reporting_template_and_context_when_all_reported(self):
        self.web_client.reported = True
        self.web_client.save()
        response = self.client.get(reverse('reporting'))

        self.assertTemplateUsed(response, 'reporting/reporting.html')
        self.assertTrue(response.context['all_reported'])
        self.assertIsNotNone(response.context['object_list'])

    def test_reporting_add_archive_template_and_action(self):
        self.web_client.reported = True
        self.web_client.save()
        response = self.client.get(reverse('add archive'))
        self.web_client.refresh_from_db()

        self.assertRedirects(response, '/reporting/')
        self.assertFalse(self.web_client.reported)
        self.assertEqual(Archive.objects.count(), 1)

    def test_reporting_report_client_with_incorrect_units(self):
        self.client.get(reverse('reporting'), data={'id': self.web_client.pk, 'units': 5})
        self.web_client.refresh_from_db()

        self.assertFalse(self.web_client.reported)

    def test_reporting_report_client_with_correct_units(self):
        self.client.get(reverse('reporting'), data={'id': self.web_client.pk, 'units': 15})
        self.web_client.refresh_from_db()

        self.assertTrue(self.web_client.reported)

    def test_reporting_report_master_with_incorrect_units(self):
        self.client.get(reverse('reporting'), data={'m_units': 200})
        self.master.refresh_from_db()

        self.assertFalse(self.master.reported)

    def test_reporting_report_master_with_correct_units(self):
        self.client.get(reverse('reporting'), data={'m_units': 400})
        self.master.refresh_from_db()

        self.assertTrue(self.master.reported)


class ReportingViewEditUnitsTest(TestCase):
    def create_user_and_client(self, username, password):
        user = User.objects.create_user(username=username, password=password)
        web_client = Client.objects.create(names='client - ' + username,
                              phone='123456789',
                              old=0,
                              new=10,
                              username=User.objects.get(username=username))
        return user, web_client

    def setUp(self):
        permission = Permission.objects.get(codename='add_archive')
        self.user, self.web_client = self.create_user_and_client('reporter', 'aw3edcvb')
        self.user.user_permissions.add(permission)
        self.client.login(username='reporter', password='aw3edcvb')
        self.master = Master.objects.create(old=100, new=300)
        Taxes.objects.create(price=0.5, tax=5)
        self.web_clients = Client.objects.all()

    def test_reporting_edit_units_template(self):
        response = self.client.get(reverse('edit units'))

        self.assertTemplateUsed(response, 'reporting/edit-units.html')

    def test_reporting_edit_units_with_incorrect_units(self):
        self.client.get(reverse('edit units'), data={'client_pk': self.web_client.pk, 'new_units': -4})
        self.web_client.refresh_from_db()

        self.assertEqual(self.web_client.new, 10)

    def test_reporting_edit_units_with_correct_units(self):
        self.client.get(reverse('edit units'), data={'client_pk': self.web_client.pk, 'new_units': 20})
        self.web_client.refresh_from_db()

        self.assertEqual(self.web_client.new, 20)


class ReportingViewEditMasterTest(TestCase):
    def create_user_and_client(self, username, password):
        user = User.objects.create_user(username=username, password=password)
        web_client = Client.objects.create(names='client - ' + username,
                              phone='123456789',
                              old=0,
                              new=10,
                              username=User.objects.get(username=username))
        return user, web_client

    def setUp(self):
        permission = Permission.objects.get(codename='add_archive')
        self.user, self.web_client = self.create_user_and_client('reporter', 'aw3edcvb')
        self.user.user_permissions.add(permission)
        self.client.login(username='reporter', password='aw3edcvb')
        self.master = Master.objects.create(old=100, new=300)
        Taxes.objects.create(price=0.5, tax=5)
        self.web_clients = Client.objects.all()

    def test_reporting_edit_master_get(self):
        response = self.client.get(reverse('edit master', kwargs={'pk': self.master.pk}))

        self.assertTemplateUsed(response, 'reporting/edit-master.html')

    def test_reporting_edit_master_post_incorrect_units(self):
        self.client.post(reverse('edit master', kwargs={'pk': self.master.pk}), data={'old': 300, 'new': 200})

        self.master.refresh_from_db()
        self.assertEqual(self.master.new, 300)

    def test_reporting_edit_master_post_correct_units(self):
        self.client.post(reverse('edit master', kwargs={'pk': self.master.pk}), data={'old': 300, 'new': 400})

        self.master.refresh_from_db()
        self.assertEqual(self.master.new, 400)


