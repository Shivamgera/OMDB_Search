from django.urls import path, include
from .views import cat

urlpatterns = [
    path('', cat),
]
