import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class MovieTestCase(APITestCase):

    def test_get_movie_endpoint_exist(self, method):
        """Movie endpoint availability."""
        http_method = self.client.__getattribute__(method)
        response = http_method(reverse('movie-list'))
        self.assertGreaterEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.skip("TODO")
    def test_create_valid_movie(self, title, movie):
        pass

    @pytest.mark.skip("TODO")
    def test_create_movie_no_title(self, title, movie):
        pass

    @pytest.mark.skip("TODO")
    def test_create_movie_already_in_database(self, title, movie):
        pass

    @pytest.mark.skip("TODO")
    def test_no_existing_movie(self):
        movie_title = 'QWERTYUIOP'

    @pytest.mark.skip("TODO")
    def test_top_movies_no_date_range(self):
        movie_title = 'QWERTYUIOP'

    @pytest.mark.skip("TODO")
    def test_top_movies_no_start_date_range(self):
        movie_title = 'QWERTYUIOP'

    @pytest.mark.skip("TODO")
    def test_top_movies_no_end_date_range(self):
        movie_title = 'QWERTYUIOP'

    @pytest.mark.skip("TODO")
    def test_top_movies_no_start_date_range(self):
        movie_title = 'QWERTYUIOP'
