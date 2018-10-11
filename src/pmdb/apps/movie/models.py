from django.db import models
from django_extensions.db.models import TimeStampedModel


class Rating(TimeStampedModel):
    """"""
    source = models.CharField(max_length=255)
    value = models.CharField(max_length=32)

    def __str__(self):
        return self.source

    def __repr__(self):
        return "<{} {}>".format(
            self.__class__.__name__, self.source
        )


class Actor(TimeStampedModel):
    """"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{} {}>".format(
            self.__class__.__name__, self.name
        )


class Director(TimeStampedModel):
    """"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{} {}>".format(
            self.__class__.__name__, self.name
        )


class Genre(TimeStampedModel):
    """"""
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{} {}>".format(
            self.__class__.__name__, self.name
        )


class Movie(TimeStampedModel):
    """"""

    title = models.CharField(max_length=255)
    year = models.IntegerField(blank=True)
    rated = models.CharField(max_length=32, blank=True)
    released = models.DateField(blank=True)
    runtime = models.CharField(max_length=16, blank=True)
    genre = models.ManyToManyField(Genre, related_name='movies')
    director = models.ManyToManyField(Director, related_name='movies')
    writer = models.TextField(blank=True)
    actors = models.ManyToManyField(Actor, related_name='movies')
    plot = models.TextField(blank=True)
    language = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)
    awards = models.CharField(max_length=255, blank=True)
    poster = models.URLField(max_length=255, blank=True)
    ratings = models.ManyToManyField(Rating, related_name='movies')
    metascore = models.CharField(max_length=16, blank=True)
    imdb_rating = models.CharField(max_length=32, blank=True)
    imdb_votes = models.CharField(max_length=32, blank=True)
    imdb_id = models.CharField(max_length=32, blank=True)
    type = models.CharField(max_length=64, blank=True)
    dvd = models.DateField(blank=True, null=True)
    box_office = models.CharField(max_length=255, blank=True)
    production = models.CharField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)
    total_seasons = models.CharField(max_length=255)
    comments_counter = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<{} {}>".format(
            self.__class__.__name__, self.title
        )


class Comment(TimeStampedModel):
    body = models.TextField()
    movie = models.ForeignKey(Movie, related_name='comments')

    def __str__(self):
        return self.body

    def __repr__(self):
        return "<{} {}>".format(
            self.__class__.__name__, self.body
        )
