from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class UserProfileAPITest(TestCase):
    """Тесты для профиля пользователя"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            phone='+79991234567',
            city='Москва'
        )

    def test_get_user_profile(self):
        """Тест получения профиля"""
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['city'], 'Москва')

    def test_update_user_profile(self):
        """Тест обновления профиля"""
        update_data = {
            'phone': '+79999999999',
            'city': 'Санкт-Петербург'
        }
        response = self.client.patch(f'/api/users/{self.user.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '+79999999999')
        self.assertEqual(self.user.city, 'Санкт-Петербург')
