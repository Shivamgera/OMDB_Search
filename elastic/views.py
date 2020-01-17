from elasticsearch_dsl import Q, Search
from rest_framework.generics import ListAPIView
from .serializers import MoviesElasticSerializer
from .elastic_index import MoviesIndex, ELASTIC_INDEX
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MoviesDocumentSerializer
from .elastic_index import MoviesAutoIndex, ELASTIC_INDEX
from .models import Movies
from .documents import MoviesDocument
from elastic.elastic_index_s import MoviesIndex
from .serializers import MoviesDocumentSerializer
from rest_framework.pagination import CursorPagination
from rest_framework import filters, response
from elasticsearch_dsl import Q
from elasticsearch_dsl import Search


class MoviesAutoCompleteView(APIView):
    serializer_class = MoviesDocumentSerializer
    pagination_class = CursorPagination
    # filter_backends = [ filters.OrderingFilter]
    # search_fields = ['title']
    # ordering = ['title', 'id']
    def get(self,request):
        param = self.request.query_params.get('q', None)
        s = MoviesIndex.search()
        # s = s.suggest('auto_complete', param, completion={'field': 'suggest'})
        # resp = s.execute()
        # print(resp)
        # if param is not None:
        #     if len(param)==0:
        #         return s[:s.count()].to_queryset()
        #     s = MoviesDocument.search().filter(Q('match',title=param) | Q('match',genre=param))
        #     return s[:s.count()].to_queryset()
        if param is not None:
            s = s.suggest('auto_complete', param, completion={'field': 'suggest'})
            resp = s.execute()
            list_resp =[]
            
            for option in resp.suggest.auto_complete[0].options:
                response_indict=dict()
                response_indict['title']=option._source.title
                response_indict['year']=option._source.year
                response_indict['rating']=option._source.rating
                response_indict['genre']=option._source.genre
                list_resp.append(response_indict)
                # response_indict.clear()
            
            # json.dumps(list)
            return Response(list_resp)
        else:
            s = MoviesIndex.search()
            return s[:s.count()].to_queryset()


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