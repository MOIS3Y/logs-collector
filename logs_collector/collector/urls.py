from django.urls import path

from . import views

app_name = 'collector'

# █░█░█ █▀▀ █▄▄
# ▀▄▀▄▀ ██▄ █▄█
# -- -- -- -- --

urlpatterns = [
    # CREATE:
    path(
        'tickets/create/',
        views.CreateTicket.as_view(),
        name='create'
    ),
    path(
        'archives/upload/',
        views.ArchiveUploadView.as_view(),
        name='upload'
    ),
    # READ:
    path(
        '',
        views.ListAllTickets.as_view(),
        name='index'
    ),
    path(
        'tickets/',
        views.ListAllTickets.as_view(),
        name='tickets'
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
        'archives/download/<path:path>',
        views.ArchiveHandlerView.as_view(),
        name="download"
    ),
    # UPDATE:
    path(
        'tickets/update/<slug:platform>/<int:ticket>/',
        views.UpdateTicket.as_view(),
        name='update'
    ),
]
