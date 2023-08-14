from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

from two_factor.urls import urlpatterns as tf_urls

from logs_collector import settings
from apps.account.utils import AdminSiteOTPRequiredMixinRedirectSetup


# ? 2FA patch (Admin site protection)
admin.site.__class__ = AdminSiteOTPRequiredMixinRedirectSetup


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        '',
        include('apps.collector.urls', namespace='collector')
    ),
    path(
        '',
        include(tf_urls)
    ),
    path(
        '',
        include('apps.account.urls', namespace='account')
    ),
    path(
        'api/',
        include('apps.collector.api.urls', namespace='collector_api')
    ),
]

# SWAGGER URLS:
urlpatterns += [
    # API PATTERNS
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path(
        'api/v1/schema/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/v1/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
