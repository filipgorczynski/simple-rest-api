import unittest

from apps.movie.serializers import CommentSerializer


class CommentSerializerTestCase(unittest.TestCase):
    fixtures = [
        'movies',
        'actors',
        'comments',
        'directors',
        'genres',
        'ratings',
    ]

    def test_valid_data(self):
        serializer = CommentSerializer(data={
            'movie_id': 1,
            'body': 'Yet another comment body',
        })
        self.assertTrue(serializer.is_valid(), msg=str(serializer.errors))

    def test_no_movie_id(self):
        serializer = CommentSerializer(data={
            'body': 'This is a body'
        })
        self.assertFalse(serializer.is_valid())

    def test_no_body(self):
        serializer = CommentSerializer(data={
            'movie': 1
        })
        self.assertFalse(serializer.is_valid())
