from django.contrib.auth.models import User
from django.test import TestCase

from course_project.web.forms import EditClientForm


class EditClientFormTests(TestCase):
    def test_edit_client_form_save__expect_username_field_disabled(self):
        user = User.objects.create_user(username='notice_author', password='aw3edcvb')
        data = {'username': user,
                'names': 'Notice A',
                'phone': '09876543',
                'paid': False}

        form = EditClientForm(data)
        disabled_fields = []
        for field_name, field in form.fields.items():
            if field.disabled:
                disabled_fields.append(field_name)

        self.assertEquals(disabled_fields, ['username'])

    def test_edit_client_form_save__invalid(self):
        data = {}
        form = EditClientForm(data)

        self.assertFalse(form.is_valid())