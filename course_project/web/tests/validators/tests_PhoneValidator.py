from django.core.exceptions import ValidationError
from django.test import TestCase

from course_project.web.validators import phone_validator


class PhoneValidatorTest(TestCase):
    def test_raise_errors(self):
        with self.assertRaises(ValidationError) as error:
            phone_validator('1234567')
        self.assertIsNotNone(error)

        with self.assertRaises(ValidationError) as error:
            phone_validator('12345680r7')
        self.assertIsNotNone(error)

    def test_not_raise_error(self):
        self.assertEqual(phone_validator('123456807'), None)