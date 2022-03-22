from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from course_project.web.models import Notice


class AnnounceViewTests(TestCase):
    def test_get__expect_correct_template(self):
        response = self.client.get(reverse('announce'))

        self.assertTemplateUsed(response, 'announce/announce.html')


class AddAnnounceViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='aw3edcvb')

        self.announce_data = {
            'title': 'test_title',
            'content': 'test_content',
            'author': User.objects.all().first(),
        }

    def test_get__logged_user__expect_correct_template(self):
        self.client.login(username='testuser', password='aw3edcvb')
        response = self.client.get(reverse('add announce'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'announce/add-announce.html')

    def test_get__not_logged_user__expect_fail(self):
        response = self.client.get(reverse('add announce'))

        self.assertEqual(response.status_code, 302)
        self.assertRaises(AssertionError)

    def test_post__correct_data__expect_new_data_in_db(self):
        self.client.login(username='testuser', password='aw3edcvb')
        self.client.post(reverse('add announce'), data=self.announce_data)

        notice = Notice.objects.all().first()

        self.assertEquals(self.announce_data['title'], notice.title)
        self.assertEquals(self.announce_data['content'], notice.content)
        self.assertEquals(self.announce_data['author'], notice.author)


class EditAnnounceViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='aw3edcvb')
        User.objects.create_user(username='notice_author', password='aw3edcvb')
        self.notice = Notice.objects.create(
            title='test_title',
            content='test_content',
            author=User.objects.get(username='notice_author')
        )

    def test_get__not_user__expect_redirect(self):
        self.client.login(username='testuser', password='aw3edcvb')
        response = self.client.get(reverse('edit announce', kwargs={'pk': self.notice.pk}))
        self.assertRedirects(response, '/403/')

    def test_post__new_title__expect_correct_data(self):
        self.client.login(username='notice_author', password='aw3edcvb')
        self.client.post(reverse('edit announce',
                                 kwargs={'pk': self.notice.pk}),
                                 {'title': 'New Title',
                                  'content': 'test_content',
                                  'author': User.objects.get(username='notice_author')})

        self.notice.refresh_from_db()
        self.assertEqual(self.notice.title, 'New Title')


class DeleteAnnounce(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='aw3edcvb')
        User.objects.create_user(username='notice_author', password='aw3edcvb')
        self.notice = Notice.objects.create(
            title='test_title',
            content='test_content',
            author=User.objects.get(username='notice_author')
        )

    def test_get__not_user__expect_redirect(self):
        self.client.login(username='testuser', password='aw3edcvb')
        response = self.client.get(reverse('delete announce', kwargs={'pk': self.notice.pk}))
        self.assertRedirects(response, '/403/')

    def test_post__delete__expect_correct_data_and_redirect(self):
        self.client.login(username='notice_author', password='aw3edcvb')
        response = self.client.post(reverse('delete announce', args=(self.notice.pk,)), follow=True)
        notices = Notice.objects.all()

        self.assertEqual(list(notices), [])
        self.assertRedirects(response, reverse('announce'), status_code=302)

    def test_get__delete_request(self):
        self.client.login(username='notice_author', password='aw3edcvb')
        response = self.client.get(reverse('delete announce', args=(self.notice.pk,)), follow=True)

        self.assertEqual(response.status_code, 200)
