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


    def test_course_serializer_returns_lessons_count(self):
        """Задание 1: поле lessons_count через SerializerMethodField"""
        course = Course.objects.create(**self.course_data)
        # Создаём 3 урока через ORM (объект, а не ID)
        for i in range(3):
            Lesson.objects.create(
                title=f'Урок {i + 1}',
                description=f'Описание урока {i + 1}',
                course=course,
                video_url=f'https://youtube.com/watch?v={i}'
            )
        response = self.client.get(f'/api/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('lessons_count', response.data)
        self.assertEqual(response.data['lessons_count'], 3)

    def test_course_serializer_returns_nested_lessons(self):
        """Задание 3: вложенный список уроков через LessonSerializer(many=True)"""
        course = Course.objects.create(**self.course_data)
        Lesson.objects.create(
            title='Урок 1: Введение',
            description='Знакомство',
            course=course,
            video_url='https://youtube.com/watch?v=1'
        )
        response = self.client.get(f'/api/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('lessons', response.data)
        self.assertIsInstance(response.data['lessons'], list)
        self.assertEqual(len(response.data['lessons']), 1)
        self.assertEqual(response.data['lessons'][0]['title'], 'Урок 1: Введение')

    def test_course_serializer_returns_both_count_and_lessons(self):
        """Один сериализатор отдаёт и lessons_count, и lessons одновременно"""
        course = Course.objects.create(**self.course_data)
        Lesson.objects.create(
            title='Урок 1', description='Описание',
            course=course, video_url='https://test.com'
        )
        response = self.client.get(f'/api/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Оба поля присутствуют одновременно
        self.assertIn('lessons_count', response.data)
        self.assertIn('lessons', response.data)
        self.assertEqual(response.data['lessons_count'], 1)
        self.assertEqual(len(response.data['lessons']), 1)


class LessonAPITest(TestCase):
    """Тесты для Lesson Generic Views"""

    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание'
        )
        self.lesson_api_data = {
            'title': 'Тестовый урок',
            'description': 'Описание урока',
            'video_url': 'https://youtube.com/watch?v=test',
            'course': self.course.id,
        }
        self.lesson_orm_data = {
            'title': 'Тестовый урок',
            'description': 'Описание урока',
            'video_url': 'https://youtube.com/watch?v=test',
            'course': self.course,
        }

    def test_create_lesson(self):
        """Тест создания урока"""
        response = self.client.post('/api/lessons/', self.lesson_api_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_list_lessons(self):
        """Тест получения списка уроков"""
        Lesson.objects.create(**self.lesson_orm_data)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_lesson(self):
        """Тест получения одного урока"""
        lesson = Lesson.objects.create(**self.lesson_orm_data)
        response = self.client.get(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовый урок')

    def test_update_lesson(self):
        """Тест обновления урока"""
        lesson = Lesson.objects.create(**self.lesson_orm_data)
        update_data = {'title': 'Обновлённый урок'}
        response = self.client.patch(f'/api/lessons/{lesson.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, 'Обновлённый урок')

    def test_delete_lesson(self):
        """Тест удаления урока"""
        lesson = Lesson.objects.create(**self.lesson_orm_data)
        response = self.client.delete(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
