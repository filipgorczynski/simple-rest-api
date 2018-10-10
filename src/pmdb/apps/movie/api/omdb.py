import requests
from django.conf import settings


def search_movie_by_title(title):
    if not title:
        raise ValueError

    params = {
        'apikey': settings.OMDB_API_KEY,
        't': title
    }
    response = requests.get(settings.OMDB_ROOT_URL, params=params)
    return response.json()
