from elasticsearch_dsl import Q, Search
from rest_framework.generics import ListAPIView

from .serializers import MoviesDocumentSerializer, MoviesElasticSerializer
from .elastic_index import MoviesIndex, ELASTIC_INDEX


def _field_query(param, field):
    if not param:
        return Q()
    param = param.replace('+', ' ').split(' ')
    if field == 'title':
        query = Q('match', title=param.pop())
        for i in param:
            query &= Q('match', title=i)
    else:
        query = Q('match', genre=param.pop())
        for i in param:
            query &= Q('match', genre=i)
    return query


class MoviesView(ListAPIView):
    serializer_class = MoviesElasticSerializer
    pagination_class = None

    def get_queryset(self):
        s = Search(index=ELASTIC_INDEX)
        title_param = self.request.query_params.get('q', None)
        genre_param = self.request.query_params.get('g', None)

        title_query = _field_query(title_param, 'title')
        genre_query = _field_query(genre_param, 'genre')

        return [i.__dict__['_d_'] for i in s.filter(title_query & genre_query)]


class SuggestionsView(ListAPIView):
    serializer_class = MoviesElasticSerializer
    pagination_class = None

    def get_queryset(self):
        s = Search(index=ELASTIC_INDEX)
        title_param = self.request.query_params.get('q', None)
        s = s.suggest('auto_complete', title_param, completion={'field': 'suggest'})
        response = s.execute()
        return [{'i._source.title', 'i._score'} for i in response.suggest.auto_complete[0]]