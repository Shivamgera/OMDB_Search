from rest_framework import serializers


class MoviesElasticSerializer(serializers.Serializer):
    title = serializers.CharField()
    year = serializers.IntegerField()
    rating = serializers.FloatField()
    genre = serializers.CharField()
