from course_project.web.models import Master
from django.test import TestCase


class TestClient(TestCase):
    def test_master__difference(self):
        master = Master(
            old=99,
            new=102,
        )

        master.full_clean()
        master.save()

        self.assertEquals(master.difference, 3)