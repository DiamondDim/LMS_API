from django.urls import path
from .views import UserProfileRetrieveUpdateAPIView

urlpatterns = [
    path('users/<int:pk>/', UserProfileRetrieveUpdateAPIView.as_view(), name='user-profile'),
]
