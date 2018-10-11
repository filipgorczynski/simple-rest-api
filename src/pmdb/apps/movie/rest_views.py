from django.db import transaction
from django.db.models import F

from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.movie.api.omdb import search_movie_by_title
from apps.movie.exceptions import MovieNotFoundException
from apps.movie.filters import CommentFilter, MovieFilter
from apps.movie.models import Movie, Comment
from apps.movie.serializers import (
    CommentSerializer,
    MovieGetSerializer,
    MoviePostSerializer,
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
            'boxOffice': 'box_office',
        }
        new_dict = {
            key.lower(): value for key, value in resp.items()
            if key not in special_cases
        }
        for key, new_key in special_cases.items():
            if resp.get(key):
                new_dict[new_key] = resp[key]
        return new_dict

    def create(self, request):
        """
        """
        serializer = MoviePostSerializer(data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            response = search_movie_by_title(title)
            if response.get('Response') == 'False':
                raise MovieNotFoundException()

            self._fix_field_names(response)

            try:
                Movie.objects.get(title=title)
            except Movie.DoesNotExist:
                serializer.save()

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
        """

        """
        top_movies = Movie.objects.all().order_by('-comments_counter')[:10]
        serializer = MovieGetSerializer(data=top_movies, many=True)
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
                movie = request.data.get('movie_id')
                Movie.objects.filter(pk=movie).update(
                    comments_counter=F('comments_counter') + 1
                )

                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )

        return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )
