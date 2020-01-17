from django.urls import path, include
from django.conf.urls import url
from .views import MoviesView, SuggestionsView

urlpatterns = [
    # path('movie/', MovieView.as_view(), name='search'),
    url('', MoviesView.as_view(), name='elastic_search'),
    url('suggest/', SuggestionsView.as_view(), name='suggestions'),
]