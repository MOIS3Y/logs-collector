from django.urls import path, include

from rest_framework import routers

from . import views

# ▄▀█ █▀█ █
# █▀█ █▀▀ █
# -- -- --

app_name = 'collector_api'

router = routers.DefaultRouter()
router.register(r'archives', views.ArchiveViewSet)
router.register(r'platforms', views.PlatformViewSet)
router.register(r'tickets', views.TicketViewSet)

check_urlpatterns = [
    path(
        'health/',
        views.AppHealthInfo.as_view(),
        name='app-info'
    ),
    path(
        'storage/',
        views.StorageInfo.as_view(),
        name='storage-info'
    ),
    path(
        'token/',
        views.TokenStateRoot.as_view(),
        name='token-root'
    ),
    path(
        'token/<str:token>',
        views.TokenStateInfo.as_view(),
        name='token-info'
    ),
]

urlpatterns = [
    # CRUD:
    path('v1/', include(router.urls)),
    path('v1/check/', include(check_urlpatterns)),
]
