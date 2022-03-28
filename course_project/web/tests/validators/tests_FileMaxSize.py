from django.core.exceptions import ValidationError
from django.test import TestCase

from course_project.web.validators import file_max_size


class FakeSize:
    def __init__(self, size):
        self.size = size


class FakeFile:
    def __init__(self, file_size):
        self.file = FakeSize(file_size)


BIGGER_SIZE = 5.1 * 1024 * 1024
NORMAL_SIZE = 5 * 1024 * 1024


class FileMaxSizeTest(TestCase):
    def test_raise_error(self):
        with self.assertRaises(ValidationError) as error:
            file_max_size((FakeFile(BIGGER_SIZE)))

        self.assertIsNotNone(error)

    def test_not_raise_error(self):

        self.assertEqual(file_max_size((FakeFile(NORMAL_SIZE))), None)
