from rest_framework import serializers
from search.models import Movies, Genres


class MoviesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, max_length=255)
    year = serializers.IntegerField()
    rating = serializers.FloatField()
