"""
Requires requests.get() mock as currently it tests for remote services.
"""
import pytest
from django.test import TestCase

from apps.movie.api.omdb import search_movie_by_title


VALID_MOVIE_RESPONSE = {
    "Title": "The Matrix",
    "Year": "1999",
    "Rated": "R",
    "Released": "31 Mar 1999",
    "Runtime": "136 min",
    "Genre": "Action, Sci-Fi",
    "Director": "Lana Wachowski, Lilly Wachowski",
    "Writer": "Lilly Wachowski, Lana Wachowski",
    "Actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
    "Plot": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
    "Language": "English",
    "Country": "USA",
    "Awards": "Won 4 Oscars. Another 34 wins & 48 nominations.",
    "Poster": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
    "Ratings": [
        {
            "Source": "Internet Movie Database",
            "Value": "8.7/10"
        },
        {
            "Source": "Rotten Tomatoes",
            "Value": "87%"
        },
        {
            "Source": "Metacritic",
            "Value": "73/100"
        }
    ],
    "Metascore": "73",
    "imdbRating": "8.7",
    "imdbVotes": "1,435,731",
    "imdbID": "tt0133093",
    "Type": "movie",
    "DVD": "21 Sep 1999",
    "BoxOffice": "N/A",
    "Production": "Warner Bros. Pictures",
    "Website": "http://www.whatisthematrix.com",
    "Response": "True"
}


class ApiOMDBTestCase(TestCase):

    def test_empty_title(self):
        with pytest.raises(ValueError):
            search_movie_by_title('')

    def test_search_movie_by_title_invalid_apikey(self):
        from django.conf import settings
        old_api_key = settings.OMDB_API_KEY
        settings.OMDB_API_KEY = 'INVALID'
        response = search_movie_by_title('The Matrix')
        self.assertEqual(response.get('Response'), 'False')
        self.assertEqual(response.get('Error'), "Invalid API key!")
        settings.OMDB_API_KEY = old_api_key

    def test_search_movie_by_valid_title(self):
        response = search_movie_by_title('The Matrix')
        self.assertEqual(response.get('Response'), 'True')

    def test_search_movie_by_not_existing_title(self):
        response = search_movie_by_title('QWERTYUIOP')
        self.assertEqual(response.get('Response'), 'False')
        self.assertEqual(response.get('Error'), "Movie not found!")
