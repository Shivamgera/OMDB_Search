from rest_framework.generics import ListAPIView

from .models import Movies
from .documents import MoviesDocument
from .serializers import MoviesDocumentSerializer


class MoviesView(ListAPIView):
    document = MoviesDocument
    serializer_class = MoviesDocumentSerializer
    lookup_field =