from django.contrib.auth.models import User
from django.test import TestCase

from course_project.web.forms import AddAnnounceForm


class AddAnnounceFormTests(TestCase):
    def test_add_announce_form_save__valid(self):
        user = User.objects.create_user(username='notice_author', password='aw3edcvb')
        data = {'title': 'New Title',
                'content': 'test_content',
                'author': user}

        form = AddAnnounceForm(data)
        placeholders = []
        class_name = []
        for f in form.fields.values():
            placeholders.append(f.widget.attrs['placeholder'])
            class_name.append(f.widget.attrs['class'])

        self.assertTrue(form.is_valid())
        self.assertEquals(placeholders, ['title', 'content', 'image'])
        self.assertEquals(list(set(class_name))[0], 'form-floating mb-3')
        self.assertEquals(len(set(class_name)), 1)
        
    def test_add_announce_form_save__invalid(self):
        data = {}
        form = AddAnnounceForm(data)

        self.assertFalse(form.is_valid())
