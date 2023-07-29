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
        'tickets/<slug:platform>/',
        views.ListPlatformTickets.as_view(),
        name='platform'
    ),
    path(
        'tickets/<slug:platform>/<int:ticket>/',
        views.DetailTicket.as_view(),
        name='ticket'
    ),
    path('archives/<path:path>', views.download, name="download")
]
