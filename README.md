# LMS API - Платформа для онлайн-обучения

## Описание
Бэкенд-сервер для платформы онлайн-обучения (LMS), реализованный на Django REST Framework. 
Позволяет управлять курсами, уроками и профилями пользователей через RESTful API.

## 🛠 Технологический стек
- Python 3.13
- Django 6.1.3
- Django REST Framework 3.18.3
- Pillow 13.0.0 (для работы с изображениями)
- Poetry (управление зависимостями)

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/DiamondDim/LMS_API.git
cd LMS_API
```
### 2.Установка зависимостей
```bash
poetry install
```
### 3. Активация виртуального окружения
```bash
poetry shell
```
### 4. Миграции базы данных
```bash
python manage.py migrate
```
### 5. Создание суперпользователя
```bash
python manage.py createsuperuser
```
### 6. Запуск сервера
```bash
python manage.py runserver
```
- Сервер будет доступен по адресу: **http://127.0.0.1:8000/**

## 📊 Структура проекта
```bash
lms_project/
├── config/          # Настройки проекта
├── lms/             # Приложение курсов и уроков
│   ├── models.py    # Модели Course и Lesson
│   ├── serializers.py
│   ├── views.py     # ViewSet для курсов, Generic для уроков
│   └── urls.py
├── users/           # Приложение пользователей
│   ├── models.py    # Кастомная модель User (email вместо username)
│   ├── serializers.py
│   ├── views.py     # Профиль пользователя
│   └── urls.py
└── manage.py
```
## 🔌 API Эндпоинты
###  Курсы (ViewSet)
| Команда | Описание |
|---------|----------|
| `GET /api/courses/` | Список всех курсов |
| `POST /api/courses/` | Создание курса |
| `GET /api/courses/{id}/` | Получение курса по ID |
| `PUT /api/courses/{id}/` | Полное обновление курса |
| `PATCH /api/courses/{id}/` | Частичное обновление курса |
| `DELETE /api/courses/{id}/` | Удаление курса |
###  Уроки (Generic Views)
| Команда | Описание |
|-------|----------|
| `GET /api/lessons/` | Список всех уроков |
| `POST /api/lessons/` | Создание урока |
| `GET /api/lessons/{id}/` | Получение урока по ID |
| `PUT /api/lessons/{id}/` | Полное обновление урока |
| `PATCH /api/lessons/{id}/` | Частичное обновление урока |
| `DELETE /api/lessons/{id}/` | Удаление урока |
###  Профиль пользователя
| Команда | Описание |
|-------|----------|
| `GET /api/users/{id}/` | Получение профиля |
| `PATCH /api/users/{id}/` | Обновление профиля (телефон, город, аватар) |

##  🧪 Тестирование
###  Проект покрыт тестами. Для запуска:
```bash
python manage.py test
```

## 👨‍💻 Автор

#### Дмитрий Леонтьев (DiamondDim)
#### © 2026

## 📄 Лицензия

#### MIT — Учебный проект для курса Python-разработки Skypro.

