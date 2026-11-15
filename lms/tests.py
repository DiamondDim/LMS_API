from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Lesson


class CourseAPITest(TestCase):
    """Тесты для CourseViewSet"""

    def setUp(self):
        self.client = APIClient()
        self.course_data = {
            'title': 'Тестовый курс',
            'description': 'Описание тестового курса',
        }

    def test_create_course(self):
        """Тест создания курса"""
        response = self.client.post('/api/courses/', self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.first().title, 'Тестовый курс')

    def test_list_courses(self):
        """Тест получения списка курсов"""
        Course.objects.create(**self.course_data)
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_course(self):
        """Тест получения одного курса"""
        course = Course.objects.create(**self.course_data)
        response = self.client.get(f'/api/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовый курс')

    def test_update_course(self):
        """Тест обновления курса"""
        course = Course.objects.create(**self.course_data)
        update_data = {'title': 'Обновлённый курс'}
        response = self.client.patch(f'/api/courses/{course.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(course.title, 'Обновлённый курс')

    def test_delete_course(self):
        """Тест удаления курса"""
        course = Course.objects.create(**self.course_data)
        response = self.client.delete(f'/api/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class LessonAPITest(TestCase):
    """Тесты для Lesson Generic Views"""

    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание'
        )
        # Данные для API-запросов (POST) - используем ID курса
        self.lesson_api_data = {
            'title': 'Тестовый урок',
            'description': 'Описание урока',
            'video_url': 'https://youtube.com/watch?v=test',
            'course': self.course.id,  # Для API передаём ID
        }
        # Данные для ORM-создания - используем объект курса
        self.lesson_orm_data = {
            'title': 'Тестовый урок',
            'description': 'Описание урока',
            'video_url': 'https://youtube.com/watch?v=test',
            'course': self.course,  # Для ORM передаём объект
        }

    def test_create_lesson(self):
        """Тест создания урока"""
        response = self.client.post('/api/lessons/', self.lesson_api_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_list_lessons(self):
        """Тест получения списка уроков"""
        Lesson.objects.create(**self.lesson_orm_data)  # Используем ORM-данные
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_lesson(self):
        """Тест получения одного урока"""
        lesson = Lesson.objects.create(**self.lesson_orm_data)  # Используем ORM-данные
        response = self.client.get(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовый урок')

    def test_update_lesson(self):
        """Тест обновления урока"""
        lesson = Lesson.objects.create(**self.lesson_orm_data)  # Используем ORM-данные
        update_data = {'title': 'Обновлённый урок'}
        response = self.client.patch(f'/api/lessons/{lesson.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, 'Обновлённый урок')

    def test_delete_lesson(self):
        """Тест удаления урока"""
        lesson = Lesson.objects.create(**self.lesson_orm_data)  # Используем ORM-данные
        response = self.client.delete(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
