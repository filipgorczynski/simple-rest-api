import pytest
from parameterized import parameterized
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class CommentTestCase(APITestCase):

    @parameterized.expand([
        ('get', status.HTTP_200_OK),
        ('post', status.HTTP_201_CREATED),
        ('put', status.HTTP_404_NOT_FOUND),
        ('delete', status.HTTP_404_NOT_FOUND),
    ])
    def test_comment_endpoint_exist(self, method, expected_status):
        """Comment endpoint availability."""
        http_method = self.client.__getattribute__(method)
        response = http_method(reverse('comment-list'))
        self.assertGreaterEqual(response.status_code, expected_status)

    @pytest.mark.skip("TODO")
    def test_create_comment(self, comment):
        self.assertFalse(True)

    @pytest.mark.skip("TODO")
    def test_create_comment_invalid_movie_id(self, comment):
        pass

    @pytest.mark.skip("TODO")
    def test_create_comment_no_movie(self, comment):
        pass

    @pytest.mark.skip("TODO")
    def test_create_comment_no_body(self, comment):
        pass
