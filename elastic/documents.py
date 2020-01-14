from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from .models import Movies, Genres

MOVIES_INDEX = Index('Movies')
MOVIES_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@MOVIES_INDEX.doc_type
class MoviesDocument(Document):
    created = fields.DateField()
    title = fields.TextField(
        fields={
            'raw': fields.TextField(analyzer='keyword')
        }
    )
    year = fields.IntegerField()
    rating = fields.FloatField()
    genre = fields.TextField(
        fields={
            'raw': fields.TextField(analyzer='keyword')
        }
    )

    class Django(object):
        model = Movies


GENRES_INDEX = Index('Genres')
GENRES_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0
)