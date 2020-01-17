from rest_framework import serializers
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


class MoviesElasticSerializer(serializers.Serializer):
    title = serializers.CharField()
    year = serializers.IntegerField()
    rating = serializers.FloatField()
    genre = serializers.CharField()