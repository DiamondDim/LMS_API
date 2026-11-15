from django.urls import path
from .views import UserProfileRetrieveUpdateAPIView, PaymentListAPIView

urlpatterns = [
    path('users/<int:pk>/', UserProfileRetrieveUpdateAPIView.as_view(), name='user-profile'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
]
