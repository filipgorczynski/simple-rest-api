import pytest
from mock import mock
from parameterized import param, parameterized
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.movie.models import Movie
from apps.movie.rest_views import MovieViewSet
from apps.movie.tests.test_api_omdb import VALID_MOVIE_RESPONSE


class MovieTestCase(APITestCase):
    # FIXME: 'ManyToManyRel' object has no attribute 'to_python':
    # FIXME: (movie.Actor:pk=2) field_value was '[1]'
    # fixtures = [
    #     'movies',
    #     'actors',
    #     'directors',
    #     'genres',
    #     'ratings',
    # ]

    @mock.patch(
        target='apps.movie.rest_views.search_movie_by_title',
        return_value=VALID_MOVIE_RESPONSE
    )
    def test_create_valid_movie(self, search_movie_by_title):
        """"""
        self.client.post(
            reverse('movie-list'),
            data={'title': 'The Matrix', }
        )
        counter = Movie.objects.filter(title='The Matrix').count()
        self.assertEqual(counter, 1)
        # FIXME self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_return_all_movies(self):
        response = self.client.get(reverse('movie-list'))
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
    @mock.patch(
        target='apps.movie.rest_views.search_movie_by_title',
        return_value=VALID_MOVIE_RESPONSE
    )
    def test_create_movie_already_in_database(self):
        movie = {
            'title': 'The Matrix',
        }
        response = self.client.post(
            reverse('movie-list'),
            data=movie
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.skip("TODO")
    def test_no_existing_movie(self):
        response = self.client.post(
            reverse('movie-list'),
            data={'title': 'QWERTYUIOP'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @parameterized.expand([
        param({}, {}),
        param(
            {'first_name': 'John', 'Title': 'The Matrix'},
            {'first_name': 'John', 'title': 'The Matrix'}
        ),
        param({'Title': 'The Matrix'}, {'title': 'The Matrix'}),
        param({'imdbID': 'tt0133093'}, {'imdb_id': 'tt0133093'}),
        param({'DVD': '2014-12-01'}, {'dvd': '2014-12-01'}),
        param({'BoxOffice': 'True'}, {'box_office': 'True'}),
    ])
    def test_fix_field_names(self, resp, expected):
        self.assertDictEqual(
            MovieViewSet._fix_field_names(resp),
            expected
        )

    @parameterized.expand([
        param({}, {}),
        param({'released': '12 Jan 2018'}, {'released': '2018-01-12'}),
        # param({'released': '33 Mod 9999'}, {'released': '2018-01-12'}),
        param({'dvd': '12 Jan 2018'}, {'dvd': '2018-01-12'}),
        param({'DVD': '12 Jan 2018'}, {'DVD': '12 Jan 2018'}),
        param({'Django': '12 Jan 2018'}, {'Django': '12 Jan 2018'}),
        param(
            {
                'Django': '12 Jan 2018',
                'released': '12 Jan 2018'
            },
            {
                'Django': '12 Jan 2018',
                'released': '2018-01-12'
            }
        ),
    ])
    def test_convert_dates(self, resp, expected):
        self.assertDictEqual(MovieViewSet._convert_dates(resp), expected)
