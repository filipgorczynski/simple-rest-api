from django_filters import NumberFilter
from django_filters.rest_framework import FilterSet

from apps.movie.models import Movie


class MovieFilter(FilterSet):
    year = NumberFilter(name='year')
    # doer_id = NumberFilter(name='employee_doer__id')
    # both_id = NumberFilter(method='filter_both')

    class Meta:
        model = Movie
        fields = {
            'year',
        }
    #
    # def filter_both(self, queryset, name, value):
    #     return queryset.filter(
    #         Q(employee_owner__id=value) | Q(employee_doer__id=value)
    #     )
