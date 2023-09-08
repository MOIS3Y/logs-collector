from django import forms
from django_filters.rest_framework import (
    CharFilter,
    FilterSet,
    NumberFilter,
    BaseInFilter,
)
from django_filters import widgets

from collector.models import Archive, Ticket
from .utils import DateTimeFilterMixin


class TextareaCSVWidget(widgets.BaseCSVWidget, forms.Textarea):
    """
    The widget should create textarea.
    """
    def render(self, name, value, attrs=None, renderer=None):
        print("Row value: ", value)
        if not self._isiterable(value):
            value = [value]

        if len(value) <= 1:
            # delegate to main widget (Select, etc...) if not multiple values
            value = value[0] if value else ''
            return super(TextareaCSVWidget, self).render(name, value, attrs)

        value = ','.join(value)
        return super(TextareaCSVWidget, self).render(name, value, attrs)


class NumberInFilter(BaseInFilter, NumberFilter):
    """
    The filter should accept coma separated integers.
    """
    pass


class ArchiveFilter(DateTimeFilterMixin, FilterSet):

    class Meta:
        model = Archive
        fields = {
            'id': ['exact', 'lte', 'gte'],
            'ticket': ['exact', 'lte', 'gte'],
            'time_create': ['exact', 'lte', 'gte']
        }


class TicketFilter(DateTimeFilterMixin, FilterSet):
    number = NumberInFilter(
        field_name='number',
        widget=TextareaCSVWidget(),
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
