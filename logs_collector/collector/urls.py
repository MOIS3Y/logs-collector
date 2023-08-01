from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.ListAllTickets.as_view(),
        name='index'
    ),
    path(
        'tickets/',
        views.ListAllTickets.as_view(),
        name='index'
    ),
    path(
        'tickets/show/<slug:platform>/',
        views.ListPlatformTickets.as_view(),
        name='platform'
    ),
    path(
        'tickets/show/<slug:platform>/<int:ticket>/',
        views.DetailTicket.as_view(),
        name='ticket'
    ),
    path(
        'archives/<path:path>',
        views.ArchiveHandlerView.as_view(),
        name="download"
    ),
]
