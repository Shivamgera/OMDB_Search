from elasticsearch_dsl import Q
from rest_framework.pagination import CursorPagination
from rest_framework.generics import ListAPIView
from rest_framework import filters

from .documents import MoviesDocument
from .serializers import MoviesDocumentSerializer


class MoviesView(ListAPIView):
    document = MoviesDocument
    serializer_class = MoviesDocumentSerializer
    pagination_class = CursorPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['title', 'id']

    def get_queryset(self):
        s = MoviesDocument.search()
        param = self.request.query_params.get('q', None)
        if param:
            temp = s.filter(Q('match', title=param) | Q('match', genre=param))
            return temp.to_queryset()
        return s[:s.count()].to_queryset()