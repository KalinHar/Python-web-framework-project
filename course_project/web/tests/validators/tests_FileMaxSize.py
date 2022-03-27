from django.core.exceptions import ValidationError
from django.test import TestCase

from course_project.web.validators import file_max_size


class BiggerSize:
    size = 5.1 * 1024 *1024


class FakeBiggerFile:
    file = BiggerSize()


class NormalSize:
    size = 5 * 1024 *1024


class FakeNormalFile:
    file = NormalSize()


class FileMaxSizeTest(TestCase):
    def test_raise_error(self):
        with self.assertRaises(ValidationError) as error:
            file_max_size(FakeBiggerFile())

        self.assertIsNotNone(error)

    def test_not_raise_error(self):
        self.assertEqual(file_max_size(FakeNormalFile()), None)
