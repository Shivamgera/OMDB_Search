from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from elastic.documents import MoviesDocument

class MoviesDocumentSerializer(DocumentSerializer):
    class Meta:
        document = MoviesDocument
        fields = (
            'title',
            'year',
            'rating',
            'genre'
        )
