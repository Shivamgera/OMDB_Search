from rest_framework import serializers


class MoviesDocumentSerializer(serializers.Serializer):
    title = serializers.CharField()
    year = serializers.IntegerField()
    rating = serializers.FloatField()
    genre = serializers.CharField()

class MoviesSuggestionsSerializer(serializers.Serializer):
    title = serializers.CharField()
    score = serializers.IntegerField()