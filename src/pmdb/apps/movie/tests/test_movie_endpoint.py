import pytest
from parameterized import param, parameterized
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.movie.models import Movie
from apps.movie.rest_views import MovieViewSet


class MovieTestCase(APITestCase):

    @pytest.mark.skip("TODO")
    def test_create_valid_movie(self):
        """
        TODO: mock request query
        """
        movie = {
            'title': 'Matrix',
        }
        response = self.client.post(
            reverse('movie-list'),
            data=movie
        )
        counter = Movie.objects.filter(title='Matrix').count()
        self.assertEqual(counter, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_movie_no_title(self):
        movie = {
            'year': '2018',
        }
        response = self.client.post(
            reverse('movie-list'),
            data=movie
        )
        counter = Movie.objects.filter(title='Matrix').count()
        self.assertEqual(counter, 0)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_top_movies(self):
        response = self.client.get(
            reverse('movie-top')
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    @pytest.mark.skip("TODO")
    def test_create_movie_already_in_database(self):
        movie = {
            'title': 'The Matrix',
        }
        response = self.client.post(
            reverse('movie-create'),
            data=movie
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.skip("TODO")
    def test_no_existing_movie(self):
        movie_title = 'QWERTYUIOP'

    @pytest.mark.skip("TODO")
    def test_top_movies_no_start_date_range(self):
        movie_title = 'QWERTYUIOP'

    @parameterized.expand([
        param({}, {}),
        param(
            {'first_name': 'John', 'Title': 'The Matrix'},
            {'first_name': 'John', 'title': 'The Matrix'}
        ),
        param({'Title': 'The Matrix'}, {'title': 'The Matrix'}),
        param({'imdbID': 'tt0133093'}, {'imdb_id': 'tt0133093'}),
        param({'DVD': '2014-12-01'}, {'dvd': '2014-12-01'}),
        param({'boxOffice': 'True'}, {'box_office': 'True'}),
    ])
    def test_fix_field_names(self, resp, expected):
        self.assertDictEqual(
            MovieViewSet._fix_field_names(resp),
            expected
        )

