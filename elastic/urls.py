from django.urls import path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# from elastic.views import MoviesDocumentViewSet
from elastic.views import MoviesView, MoviesAutoCompleteView
# from rest_framework_extensions.routers import ExtendedDefaultRouter

# router = ExtendedDefaultRouter()
# # movies = router.register(r'elasticsearch',
# #                         MoviesDocumentViewSet,
# #                         base_name='moviesdocument')
urlpatterns = [
    # path('movie/', MovieView.as_view(), name='search'),
    url(r'^', include(router.urls)),
    path('search/', MoviesView.as_view(), name='movies'),
    path('auto_complete/', MoviesAutoCompleteView.as_view(), name='suggest'),
]
