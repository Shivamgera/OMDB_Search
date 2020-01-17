import pickle
from operator import or_
from functools import reduce

from django.db.models import Q
from rest_framework.pagination import CursorPagination
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import filters

from .models import Movies
from .serializers import MoviesSerializer
# Create your views here.


@api_view()
def cat(request):
    categ = pickle.load(open('search/temp_data_dir/cat.pkl', 'rb'))
    return Response({'categories': sorted(categ)})


class MovieView(ListAPIView):
    serializer_class = MoviesSerializer
    pagination_class = CursorPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genre']
    ordering = ['title', 'rating']

    def get_queryset(self):
        query_set = Movies.objects.all()
        title_param = self.request.query_params.get('q', None)
        genre_param = self.request.query_params.get('g', None)

        title_query = _field_query(title_param, 'title')
        genre_query = _field_query(genre_param, 'genre')
        return query_set.filter(title_query & genre_query).values()


        # if param is not None:
        #     title_query_set = reduce(or_, (Q(title__icontains=i) for i in param))
        #     genre_query_set = reduce(or_, (Q(genre__icontains=i) for i in param)),
        #     query_set = query_set.filter(title_query_set & genre_query_set).values()
        # return query_set

def _field_query(param, field):
    if not param:
        return Q()
    param = param.replace('+', ' ').split(' ')
    query = Q()
    if field == 'title':
        for i in param:
            query &= Q(title__icontains=i)
    else:
        for i in param:
            query &= Q(genre__icontains=i)
    return query
