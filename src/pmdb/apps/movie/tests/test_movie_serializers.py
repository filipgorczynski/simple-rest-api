import unittest

import pytest

from apps.movie.serializers import MovieGetSerializer, MoviePostSerializer


class MoviePostSerializerTestCase(unittest.TestCase):

    def test_valid_data(self):
        serializer = MoviePostSerializer(data={
            'title': 'Sneakers',
        })
        self.assertTrue(serializer.is_valid(), msg=str(serializer.errors))

    def test_no_title(self):
        serializer = MoviePostSerializer(data={})
        self.assertFalse(serializer.is_valid())


class MovieGetSerializerTestCase(unittest.TestCase):

    @pytest.mark.skip("Test requires validation")
    def test_valid_data(self):
        serializer = MovieGetSerializer(data={
            'title': 'Sneakers',
        })
        self.assertTrue(serializer.is_valid(), msg=str(serializer.errors))
