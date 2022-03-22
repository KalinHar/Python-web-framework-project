from django.contrib.auth.models import User
from django.test import TestCase

from course_project.web.forms import EditAnnounceForm


class EditAnnounceFormTests(TestCase):
    def test_edit_announce_form_save__expect_author_field_disabled(self):
        user = User.objects.create_user(username='notice_author', password='aw3edcvb')
        data = {'title': 'New Title',
                'content': 'test_content',
                'image': '',
                'author': user}

        form = EditAnnounceForm(data)
        disabled_fields = []
        for field_name, field in form.fields.items():
            if field.disabled:
                disabled_fields.append(field_name)

        self.assertEquals(disabled_fields, ['author'])

    def test_edit_announce_form_save__invalid(self):
        data = {}
        form = EditAnnounceForm(data)

        self.assertFalse(form.is_valid())
