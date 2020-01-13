from django.urls import path, include
from .views import cat, MovieView

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', cat),
    path('movie/', MovieView.as_view(), name='search'),
]
