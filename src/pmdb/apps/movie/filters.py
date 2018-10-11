from django_filters import rest_framework as filters

from apps.movie.models import Comment, Movie


class MovieFilter(filters.FilterSet):
    year = filters.DateFromToRangeFilter(field_name="year")
    release = filters.DateFromToRangeFilter(field_name="year")

    class Meta:
        model = Movie
        fields = ['year', 'release']


class CommentFilter(filters.FilterSet):
    date_range = filters.DateFromToRangeFilter(field_name="created")

    class Meta:
        model = Comment
        fields = ['movie_id', 'date_range']
