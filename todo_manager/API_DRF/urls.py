from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import  views

app_name = 'API_DRF'

urlpatterns = [
    path('check-code/', views.TelegramProfileChekCodeView.as_view(), name='check-code'),
]
