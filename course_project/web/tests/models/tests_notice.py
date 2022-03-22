from django.contrib.auth.models import User

from course_project.web.models import Notice
from django.test import TestCase


class TestNotice(TestCase):
    def test_notice__create_correct_data__expect_success(self):
        notice = Notice(
            title='TITLE',
            content='CONTENT',
            author=User.objects.create(username='Profile',)
        )

        notice.full_clean()
        notice.save()

        self.assertIsNotNone(notice.pk)

    def test_notice__crate_incorrect_date__expect_fail(self):
        with self.assertRaises(ValueError):
            notice = Notice(
                title='TITLE',
                content='CONTENT',
                author='No Author'
            )

        self.assertRaises(AssertionError)