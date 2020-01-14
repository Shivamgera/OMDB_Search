from django.urls import path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from elastic.views import MoviesDocumentViewSet
from rest_framework_extensions.routers import ExtendedDefaultRouter

router = ExtendedDefaultRouter()
movies = router.register(r'search',
                        MoviesDocumentViewSet,
                        base_name='moviesdocument')
urlpatterns = [
    # path('movie/', MovieView.as_view(), name='search'),
    url(r'^', include(router.urls)),
]
