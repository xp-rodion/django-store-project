from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import EmailVerification, User


class UserRegistrateViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'username': 'Rodion', 'first_name': 'Rodion', 'last_name': 'Timofeev',
            'email': 'clclclc@mail.ru', 'password1': '12345678pP', 'password2': '12345678pP',
        }

    def test_user_registrate_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registrate_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check after registration user
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(email_verification.exists())
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_user_registration_post_error(self):
        username = self.data['username']
        User.objects.create(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
