from itertools import permutations

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Completion, Keyword, Float, Text

from .models import Movies


@registry.register_document
class MoviesDocument(Document):
    # title = Text(
    #     fields={
    #         'keyword': Keyword()
    #     }
    # )
    # suggest = Completion()
    # rating = Float()
    #
    # def clean(self):
    #     self.suggest = {
    #         'input': [' '.join(p) for p in permutations(self.title.split())],
    #         'weight': self.rating
    #     }

    class Index:
        name = 'movies'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django(object):
        model = Movies
        fields = [
            'year',
            'genre',
            'title',
            'rating'
        ]
