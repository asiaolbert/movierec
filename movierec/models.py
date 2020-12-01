from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class Movie(models.Model):
    movieId = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Rating(models.Model):
    userId = models.ForeignKey(User,to_field='id', on_delete=models.CASCADE)
    movieId = models.ForeignKey(Movie,to_field='movieId', on_delete=models.CASCADE)
    rating = models.FloatField()
    timestamp = models.DateTimeField()

    # def __str__(self):
    #     return self.userId + ":" + self.movieId + ":" + self.rating
class Recommendation(models.Model):
    userId = models.ForeignKey(User,to_field='id', on_delete=models.CASCADE)
    recommended_movies = models.JSONField()
