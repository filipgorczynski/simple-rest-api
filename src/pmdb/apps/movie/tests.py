from parameterized import parameterized
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestMovieEndpoint(APITestCase):

    @parameterized.expand(['get', 'post'])
    def test_endpoint_exist(self, method):
        """Endpoint availability."""
        http_method = self.client.__getattribute__(method)
        response = http_method(reverse('movie-list'))
        self.assertGreaterEqual(response.status_code, status.HTTP_200_OK)
