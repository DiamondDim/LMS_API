from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Payment
from lms.models import Course, Lesson


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
        # Авторизуем клиента — теперь 403 не будет!
        self.client.force_authenticate(user=self.user)

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


class PaymentAPITest(TestCase):
    """Тесты для модели Payment и фильтрации (Задание 2 и 4)"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание'
        )
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание',
            course=self.course,
            video_url='https://youtube.com/watch?v=test'
        )
        # Создаём платежи с разными параметрами для тестирования фильтров
        self.payment_course = Payment.objects.create(
            user=self.user,
            course=self.course,
            amount='5000.00',
            payment_method='transfer'
        )
        self.payment_lesson = Payment.objects.create(
            user=self.user,
            lesson=self.lesson,
            amount='1500.50',
            payment_method='cash'
        )
        self.payment_transfer_2 = Payment.objects.create(
            user=self.user,
            course=self.course,
            amount='7500.00',
            payment_method='transfer'
        )

    def test_list_payments(self):
        """Тест получения списка платежей"""
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_course(self):
        """Задание 4: фильтрация по курсу"""
        response = self.client.get('/api/payments/?course=' + str(self.course.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for p in response.data:
            self.assertIsNotNone(p['course'])

    def test_filter_by_lesson(self):
        """Задание 4: фильтрация по уроку"""
        response = self.client.get('/api/payments/?lesson=' + str(self.lesson.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.payment_lesson.id)

    def test_filter_by_payment_method_cash(self):
        """Задание 4: фильтрация по способу оплаты (наличные)"""
        response = self.client.get('/api/payments/?payment_method=cash')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['payment_method'], 'cash')

    def test_filter_by_payment_method_transfer(self):
        """Задание 4: фильтрация по способу оплаты (перевод)"""
        response = self.client.get('/api/payments/?payment_method=transfer')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_ordering_ascending(self):
        """Задание 4: сортировка по дате по возрастанию"""
        response = self.client.get('/api/payments/?ordering=payment_date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['id'], self.payment_course.id)

    def test_ordering_descending(self):
        """Задание 4: сортировка по дате по убыванию"""
        response = self.client.get('/api/payments/?ordering=-payment_date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['id'], self.payment_transfer_2.id)


class UserPaymentsBonusTest(TestCase):
    """Бонусное задание: история платежей в профиле пользователя"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            phone='+79991234567',
            city='Москва'
        )
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание'
        )
        Payment.objects.create(
            user=self.user,
            course=self.course,
            amount='5000.00',
            payment_method='transfer'
        )
        Payment.objects.create(
            user=self.user,
            amount='1500.50',
            payment_method='cash'
        )
        # Авторизация для доступа к профилю
        self.client.force_authenticate(user=self.user)

    def test_profile_contains_nested_payments(self):
        """Профиль пользователя содержит вложенную историю платежей"""
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('payments', response.data)
        self.assertEqual(len(response.data['payments']), 2)

    def test_payments_contain_nested_course_data(self):
        """Платежи содержат вложенные данные курса (полная вложенность)"""
        response = self.client.get(f'/api/users/{self.user.id}/')
        payments = response.data['payments']
        course_payment = next(p for p in payments if p['payment_method'] == 'transfer')
        self.assertIn('course', course_payment)
        self.assertEqual(course_payment['course']['title'], 'Тестовый курс')
