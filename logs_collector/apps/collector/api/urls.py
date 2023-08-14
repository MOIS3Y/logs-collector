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

urlpatterns = [
    # CRUD:
    path('v1/', include(router.urls)),
]
