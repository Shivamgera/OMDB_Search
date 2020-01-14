from django_elasticsearch_dsl_drf.serializers import DocumentSerializer


class MoviesDocumentSerializer(DocumentSerializer):
    class Meta:
        fields = (
            'title',
            'year',
            'rating',
            'genre'
        )
