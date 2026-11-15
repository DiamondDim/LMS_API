from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView

# Роутер автоматически создаст все пути для CourseViewSet (/lms/courses/, /lms/courses/{id}/, и т.д.)
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    # Подключаем маршруты роутера
    path('', include(router.urls)),

    # Явно прописываем маршруты для Generic-классов урока
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
]
