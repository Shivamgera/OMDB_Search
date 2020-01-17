from rest_framework.generics import ListAPIView
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
# from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
# from django_elasticsearch_dsl_drf.filter_backends import (
#     FilteringFilterBackend,
#     DefaultOrderingFilterBackend,
#     OrderingFilterBackend,
#     SearchFilterBackend,
#     SuggesterFilterBackend,
#     FunctionalSuggesterFilterBackend,
# )
# from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

# class MoviesView(ListAPIView):
#     serializer_class = MoviesDocumentSerializer
#     pagination_class = CursorPagination
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title']
#     ordering = ['title']
#     def get_queryset(self):
#         param = self.request.query_params.get('q', None)
#         s = MoviesDocument.search()
#         if param is not None:
#             if len(param)==0:
#                 return s[:s.count()].to_queryset()
#             s = MoviesDocument.search().filter(Q('match',title=param) | Q('match',genre=param))
#             return s[:s.count()].to_queryset()
#         return s[:s.count()].to_queryset()

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
    serializer_class = MoviesDocumentSerializer
    pagination_class = None
    def get_queryset(self):
        s = Search(index=ELASTIC_INDEX)
        title_param = self.request.query_params.get('q', None)
        genre_param = self.request.query_params.get('g', None)
        title_query = _field_query(title_param, 'title')
        genre_query = _field_query(genre_param, 'genre')
        return [i.__dict__['_d_'] for i in s.filter(title_query & genre_query)]

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




# class MoviesDocumentViewSet(ListAPIView):
#     document = MoviesDocument
#     serializer_class = MoviesDocumentSerializer
#     lookup_field = 'id'
#     filter_backends= [
#         # FilteringFilterBackend,
#         # DefaultOrderingFilterBackend,
#         # OrderingFilterBackend,
#         SearchFilterBackend,
#         SuggesterFilterBackend
#     ]
#     # pagination_class = CursorPagination It will cause error
#     pagination_class= LimitOffsetPagination
#     search_fields=(
#         'title',
#         'genre'
#     )
#     filter_fields = {
#         'genre:genre.raw'
#     }
#     ordering_fields = {
#         'title':'title.raw',
#         'id':None,
#     }
#     ordering = ('title','id')
#     suggester_fields = {
#         'name_suggest':{
#             'field':'title.suggest',
#             'suggesters':[
#                 SUGGESTER_TERM,
#                 SUGGESTER_PHRASE,
#                 SUGGESTER_COMPLETION,
#             ]
#         }
#     }


