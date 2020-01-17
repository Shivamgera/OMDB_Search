from django_elasticsearch_dsl import Document, Index, fields

from .models import MoviesModel

MOVIES_INDEX = Index('movies')
MOVIES_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@MOVIES_INDEX.doc_type
class MoviesDocument(Document):
    created = fields.DateField()
    title = fields.TextField(
        fields={
            'raw': fields.TextField(analyzer='keyword'),
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
        model = MoviesModel
