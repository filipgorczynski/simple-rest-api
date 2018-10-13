import pytest
from mock import mock
from parameterized import param, parameterized
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.movie.exceptions import OMDBException
from apps.movie.models import Movie
from apps.movie.rest_views import MovieViewSet
from apps.movie.tests.test_api_omdb import VALID_MOVIE_RESPONSE

EXPECTED_TOP_MOVIES = [
    {
        "movie_id": 4,
        "total_comments": 4,
        "rank": 1
    },
    {
        "movie_id": 3,
        "total_comments": 2,
        "rank": 2
    },
    {
        "movie_id": 4,
        "total_comments": 2,
        "rank": 2
    },
    {
        "movie_id": 1,
        "total_comments": 0,
        "rank": 3
    },
]


class MovieTestCase(APITestCase):
    fixtures = [
        'movies',
        'actors',
        'comments',
        'directors',
        'genres',
        'ratings',
    ]

    @mock.patch(
        target='apps.movie.rest_views.search_movie_by_title',
        return_value=VALID_MOVIE_RESPONSE
    )
    def test_create_valid_movie(self, search_movie_by_title):
        """"""
        response = self.client.post(
            reverse('movie-list'),
            data={'title': 'The Matrix', }
        )
        counter = Movie.objects.filter(title='The Matrix').count()
        self.assertEqual(counter, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_return_all_movies(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create_movie_no_title(self):
        counter = Movie.objects.all().count()
        movie = {}
        response = self.client.post(
            reverse('movie-list'),
            data=movie
        )
        self.assertEqual(counter, 4)
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
            status.HTTP_200_OK,
        )
        # FIXME: self.assertDictEqual(
        #     response.data,
        #     EXPECTED_TOP_MOVIES
        # )

    @mock.patch(
        target='apps.movie.rest_views.search_movie_by_title',
        return_value=VALID_MOVIE_RESPONSE
    )
    def test_create_movie_already_in_database(self, search_movie_mock):
        movie = {
            'title': 'Sneakers',
        }
        response = self.client.post(
            reverse('movie-list'),
            data=movie
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('imdb_id'), "tt0105435")

    def test_no_existing_movie(self):
        with pytest.raises(OMDBException):
            self.client.post(
                reverse('movie-list'),
                data={'title': 'QWERTYUIOP'}
            )

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
        MovieViewSet._convert_dates(resp)
        self.assertDictEqual(resp, expected)

    def test_convert_dates_invalid_date(self):
        with pytest.raises(ValueError):
            MovieViewSet._convert_dates({'released': '33 Mod 9999'})
