from django.urls import path, include

from rest_framework import routers

from . import views

app_name = 'collector'

router = routers.DefaultRouter()
router.register(r'archives', views.ArchiveViewSet)
router.register(r'platforms', views.PlatformViewSet)
router.register(r'tickets', views.TicketViewSet)

urlpatterns = [

    # █░█░█ █▀▀ █▄▄
    # ▀▄▀▄▀ ██▄ █▄█
    # -- -- -- -- --

    # CREATE:
    path(
        'tickets/create/',
        views.CreateTicket.as_view(),
        name='create'
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
        'archives/<path:path>',
        views.ArchiveHandlerView.as_view(),
        name="download"
    ),
    # UPDATE:
    path(
        'tickets/update/<slug:platform>/<int:ticket>/',
        views.UpdateTicket.as_view(),
        name='update'
    ),

    # ▄▀█ ░░█ ▄▀█ ▀▄▀
    # █▀█ █▄█ █▀█ █░█
    # -- -- -- -- --

    # UPDATE:
    path(
        'ajax/tickets/update/<slug:platform>/<int:ticket>/',
        views.UpdateTicketStateHandler.as_view(),
        name='ajax_update_state_ticket'
    ),
    # DELETE:
    path(
        'ajax/tickets/delete/<int:ticket>/',
        views.DeleteTicketHandler.as_view(),
        name='ajax_delete_ticket'
    ),

    # ▄▀█ █▀█ █
    # █▀█ █▀▀ █
    # -- -- --

    # CRUD:
    path('api/v1/', include(router.urls))
]
