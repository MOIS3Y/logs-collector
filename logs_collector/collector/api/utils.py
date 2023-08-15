from django_filters import NumberFilter


class DateTimeFilterMixin:
    year__gte = NumberFilter(
        field_name='time_create',
        lookup_expr='year__gte'
    )
    year__lte = NumberFilter(
        field_name='time_create',
        lookup_expr='year__lte'
    )
    month__gte = NumberFilter(
        field_name='time_create',
        lookup_expr='month__gte'
    )
    month__lte = NumberFilter(
        field_name='time_create',
        lookup_expr='month__lte'
    )
