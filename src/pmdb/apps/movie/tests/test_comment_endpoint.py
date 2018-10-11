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

    def test_create_comment(self):
        comment = {
            'body': 'This is a comment test body',
            'movie_id': 1,
        }
        response = self.client.post(
            reverse('comment-list'),
            data=comment
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_no_movie_id(self):
        comment = {
            'body': 'This is a comment test body',
        }
        response = self.client.post(
            reverse('comment-list'),
            data=comment
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_no_movie_id_in_database(self):
        comment = {
            'body': 'This is a comment test body',
            'movie_id': 99999
        }
        response = self.client.post(
            reverse('comment-list'),
            data=comment
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_no_body(self):
        comment = {
            'movie_id': 1,
        }
        response = self.client.post(
            reverse('comment-list'),
            data=comment
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
