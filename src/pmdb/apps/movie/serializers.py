from rest_framework import serializers

from .models import (
    Actor,
    Director,
    Genre,
    Movie,
    Rating,
)

Actor, Director, Genre, Movie, Rating,

class ActorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actor
        fields = ('name', 'created_at', 'updated_at',)


class DirectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Director
        fields = ('name', 'created_at', 'updated_at',)


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'created_at', 'updated_at',)


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ('source', 'value', 'created_at', 'updated_at',)


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ('__all__',)