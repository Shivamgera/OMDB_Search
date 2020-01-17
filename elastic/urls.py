from django.urls import path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from elastic.views import MoviesView, MoviesAutoCompleteView, SuggestionsView

urlpatterns = [
    #url(r'^', include(router.urls)),
    path('search/', MoviesView.as_view(), name='movies'),
    path('auto_complete/', MoviesAutoCompleteView.as_view(), name='suggest'),
    url('suggest/', SuggestionsView.as_view(), name='suggestions'),
]
