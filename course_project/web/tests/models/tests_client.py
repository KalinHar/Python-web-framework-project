from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from course_project.web.models import Client
from django.test import TestCase


class TestClient(TestCase):

    VALID_CLIENT_DATA = {
        'names': 'Pepo Petrov',
        'phone': '12345678',
        'old': 0,
        'new': 0,
    }

    def setUp(self):
        User.objects.create(username='Profile',)

    def test_client__crate_correct_data__expect_success(self):
        client = Client(
            names=self.VALID_CLIENT_DATA['names'],
            phone=self.VALID_CLIENT_DATA['phone'],
            old=self.VALID_CLIENT_DATA['old'],
            new=self.VALID_CLIENT_DATA['new'],
            username=User.objects.get(username='Profile')
        )

        client.full_clean()
        client.save()

        self.assertIsNotNone(client.pk)

    def test_client__crate_incorrect_username__expect_fail(self):

        with self.assertRaises(ValueError):
            client = Client(
                names=self.VALID_CLIENT_DATA['names'],
                phone=self.VALID_CLIENT_DATA['phone'],
                old=self.VALID_CLIENT_DATA['old'],
                new=self.VALID_CLIENT_DATA['new'],
                username='No Profile'
            )

        self.assertRaises(AssertionError)

    def test_client__crate_incorrect_phone_numbers__expect_fail(self):
        client = Client(
            names=self.VALID_CLIENT_DATA['names'],
            phone='08976453r6',
            old=self.VALID_CLIENT_DATA['old'],
            new=self.VALID_CLIENT_DATA['new'],
            username=User.objects.get(username='Profile')
        )

        with self.assertRaises(ValidationError) as context:
            client.full_clean()
            client.save()

        self.assertIsNotNone(context.exception)

    def test_client__crate_incorrect_phone_length__expect_fail(self):
        client = Client(
            names=self.VALID_CLIENT_DATA['names'],
            phone='0897645',
            old=self.VALID_CLIENT_DATA['old'],
            new=self.VALID_CLIENT_DATA['new'],
            username=User.objects.get(username='Profile')
        )

        with self.assertRaises(ValidationError) as context:
            client.full_clean()
            client.save()

        self.assertIsNotNone(context.exception)

    def test_client__difference(self):
        client = Client(
            names=self.VALID_CLIENT_DATA['names'],
            phone=self.VALID_CLIENT_DATA['phone'],
            old=5,
            new=15,
            username=User.objects.get(username='Profile')
        )

        client.full_clean()
        client.save()

        self.assertEquals(client.difference, 10)