import pickle

from django.shortcuts import render
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


"""
Movie: Title, Year, imdbRating, 
Genres: MovieID, genre
"""


class MovieView(ListAPIView):
    serializer_class = MoviesSerializer
    pagination_class = CursorPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering = ['title', 'id']

    def get_queryset(self):
        query_set = Movies.objects.all()
        param = self.request.query_params.get('q', None)
        if param is not None:
            query_set = query_set.filter(title__icontains=param).values()
        return query_set

