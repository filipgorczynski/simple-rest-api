from rest_framework import serializers

from .models import Actor, Comment, Director, Genre, Movie, Rating


class ActorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actor
        fields = ('name', 'created', 'modified',)


class DirectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Director
        fields = ('name', 'created', 'modified',)


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'created', 'modified',)


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ('source', 'value', 'created', 'modified',)


class MoviePostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ('title',)


class MovieGetSerializer(serializers.HyperlinkedModelSerializer):
    genre = GenreSerializer(many=True)
    director = DirectorSerializer(many=True)
    actors = ActorSerializer(many=True)
    ratings = RatingSerializer(many=True)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    class Meta:
        model = Movie
        fields = (
            'title', 'year', 'rated', 'released', 'runtime', 'genre',
            'director', 'writer', 'actors', 'plot', 'language', 'country',
            'awards', 'poster', 'ratings', 'metascore', 'imdb_rating',
            'imdb_votes', 'imdb_id', 'type', 'dvd', 'box_office',
            'production', 'website', 'comments_counter', 'created',
            'modified', 'total_seasons',
        )


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        fields = ('body', 'movie', 'movie_id', 'created', 'modified',)
