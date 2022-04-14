from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginFormViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='aw3edcvb')
        self.user = User.objects.all().first()

    def test_incorrect_user_login(self):
        response = self.client.login(username='testuser', password='aw3edcv')

        self.assertFalse(response)

    def test_correct_user_login(self):
        response = self.client.login(username='testuser', password='aw3edcvb')

        self.assertTrue(response)

    def test_incorrect_login_message(self):
        response = self.client.post(reverse('login'), data={'username': 'testuser', 'password': 'aw3edcv'})

        self.assertEqual(response.context['message'], 'Login failed!')



class RegisterFormViewTest(TestCase):
    def test_correct_register_temlate(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='auth/register.html')

    def test_correct_user_register(self):
        response = self.client.post(reverse('register'), data={'username': 'testuser', 'password1': 'aw3edcvb', 'password2': 'aw3edcvb'})

        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertRedirects(response, '/')

    def test_pass_not_equal_register(self):
        response = self.client.post(reverse('register'), data={'username': 'testuser', 'password1': 'aw3edcvb', 'password2': 'aw3edcv'})

        users = User.objects.all()
        self.assertEqual(users.count(), 0)
        self.assertEqual(response.context['message'], "Passwords don't match.")

    def test_pass_too_short_register(self):
        response = self.client.post(reverse('register'), data={'username': 'testuser', 'password1': 'aw3edcv', 'password2': 'aw3edcv'})

        users = User.objects.all()
        self.assertEqual(users.count(), 0)
        self.assertEqual(response.context['message'], 'Password must be at least 8 symbols.')


    def test_user_exist_register(self):
        User.objects.create_user(username='testuser', password='aw3edcvb')
        response = self.client.post(reverse('register'), data={'username': 'testuser', 'password1': 'aw3edcvb', 'password2': 'aw3edcvb'})

        self.assertEqual(response.context['message'], 'Username exist!')

    def test_user_unsuccess_register(self):
        response = self.client.post(reverse('register'), data={'username': '', 'password1': 'aw3edcvb', 'password2': 'aw3edcvb'})

        self.assertEqual(response.context['message'], 'Unsuccessful registration!')

