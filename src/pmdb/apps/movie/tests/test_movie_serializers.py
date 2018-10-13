from django.test import TestCase

from apps.movie.models import Movie
from apps.movie.serializers import MovieGetSerializer, MoviePostSerializer


class MoviePostSerializerTestCase(TestCase):

    def test_movie_post_serializer_valid_data(self):
        serializer = MoviePostSerializer(data={
            'title': 'Sneakers',
        })
        self.assertTrue(serializer.is_valid(), msg=str(serializer.errors))

    def test_movie_post_serializer_no_title(self):
        serializer = MoviePostSerializer(data={})
        self.assertFalse(serializer.is_valid())


class MovieGetSerializerTestCase(TestCase):
    fixtures = [
        'movies',
    ]

    def test_valid_data(self):
        movie = Movie.objects.get(title='Sneakers')
        serializer = MovieGetSerializer(movie)
        self.assertEqual(serializer.data.get('imdb_id'), "tt0105435")
