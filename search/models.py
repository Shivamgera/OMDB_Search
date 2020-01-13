from django.db import models
# Create your models here.

class Movies(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.title} & {self.rating}'


class Genres(models.Model):
    movie_id = models.ForeignKey('Movies', on_delete=models.CASCADE)
    genre = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.movie_id} {self.genre}'