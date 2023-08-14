from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LogoutView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


app_name = 'account'

urlpatterns = [
    # WEB LOGOUT:
    path(
        'accounts/logout/',
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name='logout'
    )
]

urlpatterns += [
    # JWT AUTH:
    path(
        'api/v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/v1/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/v1/auth/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]
