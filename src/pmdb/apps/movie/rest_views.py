from django.db.models import Count

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.movie.api.omdb import search_movie_by_title
from apps.movie.exceptions import MovieNotFoundException
from apps.movie.models import Movie, Comment
from apps.movie.serializers import (
    CommentSerializer,
    MovieGetSerializer,
    MoviePostSerializer,
)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieGetSerializer

    def create(self, request):
        """

        """
        self.serializer_class = MoviePostSerializer

        title = request.data.get('title')
        # TODO: check if movie already exists in database...
        movie = Movie.objects.get(title=title)
        if movie:
            serializer = MovieGetSerializer(data=movie)
            return Response(
                data=serializer,
            )
        if title:
            response = search_movie_by_title(title)
            if response.get('Response') == 'False':
                raise MovieNotFoundException()

            # TODO: add movie serializer validator
            # movie_serializer = self.get_serializer(data=movie)
            # try:
            #     # movie_serializer.is_valid(raise_exception=True)
            #     pass
            # except ValidationError as ex:
            #     raise

            # movie = movie_serializer.save()

        return Response(
            data="This should be whole movie object",
            status=status.HTTP_201_CREATED
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
        top_movies = Comment.objects.all().prefetch_related('movie').annotate(
            total=Count('movie_id')).order_by('-total')

        serializer = MovieGetSerializer(data=top_movies, many=True)
        serializer.is_valid()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class CommentViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request):
        """

        :param request:
        :return:
        """
        serializer = CommentSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors, status.HTTP_400_BAD_REQUEST
        )
