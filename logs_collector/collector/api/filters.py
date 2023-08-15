from django_filters.rest_framework import (
    CharFilter,
    FilterSet,
    NumberFilter,
)
from django_filters import widgets

from collector.models import Archive, Ticket
from .utils import DateTimeFilterMixin


class ArchiveFilter(DateTimeFilterMixin, FilterSet):

    class Meta:
        model = Archive
        fields = {
            'id': ['exact', 'in', 'lte', 'gte'],
            'ticket': ['exact', 'in', 'lte', 'gte'],
            'time_create': ['exact', 'lte', 'gte']
        }


class TicketFilter(DateTimeFilterMixin, FilterSet):
    number = NumberFilter(
        field_name='number',
        widget=widgets.CSVWidget(),
    )
    user = CharFilter(
        field_name='user__username'
    )

    class Meta:
        model = Ticket
        fields = {
            'id': ['exact', 'in', 'lte', 'gte'],
            'number': ['exact', 'contains', 'in', 'lte', 'gte'],
            'resolved': ['exact'],
            'user': ['exact']
        }
