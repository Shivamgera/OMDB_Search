from django.db import models


class Movies(models.Model):
    created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    rating = models.FloatField()
    genre = models.TextField(default='No Genre')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.title} & {self.rating}'
