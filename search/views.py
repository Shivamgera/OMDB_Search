import pickle

from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.


def cat(request):
    categ = pickle.load(open('search/temp_data_dir/cat.pkl', 'rb'))
    return JsonResponse({'categories': list(categ), 'movies': {}})