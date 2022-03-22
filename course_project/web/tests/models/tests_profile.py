from django.contrib.auth.models import User
from django.test import TestCase


class TestProfile(TestCase):
    def test_profile_crate__expect_success(self):
        profile = User(
            username='Test1',
        )
        profile.save()
        self.assertIsNotNone(profile.pk)
