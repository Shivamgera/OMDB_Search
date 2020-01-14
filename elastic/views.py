from rest_framework.generics import ListAPIView

from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_TERM,
    SUGGESTER_PHRASE,
    SUGGESTER_COMPLETION,
)
from .models import Movies
from .documents import MoviesDocument
from .serializers import MoviesDocumentSerializer
from rest_framework.pagination import CursorPagination
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    DefaultOrderingFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
    FunctionalSuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet



class MoviesDocumentViewSet(DocumentViewSet):
    document = MoviesDocument
    serializer_class = MoviesDocumentSerializer
    lookup_field = 'id'
    filter_backends= [
        # FilteringFilterBackend,
        DefaultOrderingFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
        # SuggesterFilterBackend
    ]
    # pagination_class = CursorPagination
    search_fields=(
        'title',
        'genre'
    )
    filter_fields = {
        'genre'
    }
    ordering_fields = {
        'title':'title',
        'id':None,
    }
    # ordering = 'title.raw'
    suggester_fields = {
        'name_suggest':{
            'field':'title.suggest',
            'suggesters':[
                SUGGESTER_TERM,
                SUGGESTER_PHRASE,
                SUGGESTER_COMPLETION,
            ]
        }
    }


