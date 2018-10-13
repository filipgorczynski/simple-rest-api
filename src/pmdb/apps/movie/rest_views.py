from datetime import datetime

from django.db import transaction
from django.db.models import F
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.movie.api.omdb import search_movie_by_title
from apps.movie.exceptions import OMDBException
from apps.movie.filters import CommentFilter, MovieFilter
from apps.movie.models import Actor, Comment, Director, Genre, Movie, Rating
from apps.movie.serializers import (
    CommentSerializer,
    MovieGetSerializer,
    MoviePostSerializer,
    MovieTopSerializer,
)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieGetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter

    @staticmethod
    def _fix_field_names(resp):
        special_cases = {
            'imdbRating': 'imdb_rating',
            'imdbVotes': 'imdb_votes',
            'imdbID': 'imdb_id',
            'DVD': 'dvd',
            'BoxOffice': 'box_office',
            'totalSeasons': 'total_seasons'
        }
        new_dict = {
            key.lower(): value for key, value in resp.items()
            if key not in special_cases
        }
        for key, new_key in special_cases.items():
            if resp.get(key):
                new_dict[new_key] = resp[key]
        return new_dict

    @staticmethod
    def _add_movie_relation(model, data, movie):
        for item in data.split(','):
            instance = model.objects.get_or_create(name=item.strip())
            instance[0].movies.add(movie)
            instance[0].save()

    @staticmethod
    def _convert_dates(resp):
        for key, value in resp.items():
            if key in {'released', 'dvd'}:
                date = datetime.strptime(value, "%d %b %Y")
                resp[key] = date.strftime("%Y-%m-%d")

    def create(self, request):
        """
        """
        serializer = MoviePostSerializer(data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            response = search_movie_by_title(title)
            if response.get('Response') == 'False':
                raise OMDBException(response.get('Error'))

            response = self._fix_field_names(response)
            self._convert_dates(response)
            try:
                movie = Movie.objects.get(title=title)
            except Movie.DoesNotExist:
                with transaction.atomic():
                    actors = response.pop('actors')
                    directors = response.pop('director')
                    genres = response.pop('genre')
                    ratings = response.pop('ratings')
                    response.pop('response')
                    movie = Movie.objects.create(**response)

                    self._add_movie_relation(Actor, actors, movie)
                    self._add_movie_relation(Director, directors, movie)
                    self._add_movie_relation(Genre, genres, movie)

                    for rating in ratings:
                        rating_instance = Rating.objects.create(
                            source=rating['Source'].strip(),
                            value=rating['Value'].strip()
                        )
                        rating_instance.movies.add(movie)
                        rating_instance.save()

                    movie.save()

            serializer = MovieGetSerializer(movie)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request):
        movies = Movie.objects.all()
        serializer = MovieGetSerializer(data=movies, many=True)
        serializer.is_valid()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @action(methods=['GET'], detail=False)
    def top(self, request):
        """"""
        top_movies = Movie.objects.all().order_by('-total_comments', 'title')
        response = []
        next_rank = prev_comment_count = 0
        for movie in top_movies:
            if movie.total_comments != prev_comment_count:
                prev_comment_count = movie.total_comments
                next_rank += 1
            response.append({
                'movie_id': movie.id,
                'total_comments': movie.total_comments,
                'rank': next_rank
            })
        serializer = MovieTopSerializer(data=response, many=True)
        serializer.is_valid()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommentFilter

    def create(self, request):
        """
        """
        serializer = CommentSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                movie_id = request.data.get('movie_id')
                try:
                    Movie.objects.get(pk=movie_id)
                except Movie.DoesNotExist:
                    return Response(
                        serializer.errors,
                        status.HTTP_400_BAD_REQUEST
                    )
                Movie.objects.filter(pk=movie_id).update(
                    total_comments=F('total_comments') + 1
                )

                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )

        return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )
