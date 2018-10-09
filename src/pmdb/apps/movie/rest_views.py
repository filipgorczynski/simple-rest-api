import logging

from django.conf import settings
from django.shortcuts import get_object_or_404

import requests
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class MovieViewSet(viewsets.ViewSet):

    def create(self, request):
        """

        """
        movie = None
        title = request.data.get('title')
        if title:
            params = {
                'apikey': settings.OMDB_API_KEY,
                't': title
            }
            if request.data.get('year'):
                params.update({'y': request.data.get('title')})

            response = requests.get(settings.OMDB_ROOT_URL, params=params)
            logger.debug("Response for {}: {}".format(title, response))
            # movie_serializer = self.get_serializer(data=request.data)
            try:
                # movie_serializer.is_valid(raise_exception=True)
            except ValidationError as ex:
                raise

            #movie = movie_serializer.save()

        return Response(
            data=self.get_serializer(movie).data,
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk):
        """
        GET request handler for specific recipe id.
        This method returns a formatted recipe structure for the recipe
        requested or returns a 404 if the recipe does not exist or 403 if the
        user is from another company
        """

        movie = get_object_or_404(self.get_queryset(), pk=pk)

        serializer = self.get_serializer(movie)
        return Response(serializer.data, status.HTTP_200_OK)

    def list(self, request):

        return Response("Movie View Set List")

#
#
# class Movie(generics.ListCreateAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#
#     def get_queryset(self):
#         columns = Column.objects.filter(board_id=self.kwargs['board_pk'])
#         queryset = Card.objects.filter(column__in=columns)
#         return queryset
#
#     def post(self, request, *args, **kwargs):
#         board = Board.objects.get(pk=kwargs['board_pk'])
#
#         post_data = {
#             'title': request.data.get('title'),
#             'description': request.data.get('description'),
#             'created_by': request.data.get('created_by'),
#             'assignees': request.data.get('assignees'),
#             'labels': request.data.get('labels'),
#         }
#         serializer = MovieSerializer(data=post_data, context={'board': board})
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status.HTTP_201_CREATED)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)