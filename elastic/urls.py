from django.urls import path, include
from django.conf.urls import url
# from elastic.views import MoviesDocumentViewSet
# from rest_framework_extensions.routers import ExtendedDefaultRouter
from .views import MoviesView


#
# router = ExtendedDefaultRouter()
# movies = router.register(r'search',
#                         MoviesDocumentViewSet,
#                         basename='moviesdocument')

urlpatterns = [
    # path('movie/', MovieView.as_view(), name='search'),
    url('', MoviesView.as_view(), name='elastic_search'),
]