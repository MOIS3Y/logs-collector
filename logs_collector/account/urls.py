from django.conf import settings
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views


app_name = 'account'

urlpatterns = [
    # WEB LOGOUT:
    path(
        'account/logout/',
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name='logout'
    ),
    # CHANGE PASSWORD:
    path(
        'account/password-change/',
        PasswordChangeView.as_view(
            template_name='account/password_change.html',
            success_url=reverse_lazy('account:password_change_done'),
        ),
        name='password_change'
    ),
    path(
        'account/password-change/done/',
        PasswordChangeDoneView.as_view(
            template_name='account/password_change_done.html'
        ),
        name='password_change_done'
    ),
    # UPDATE:
    path(
        'account/update/',
        views.UpdateProfile.as_view(),
        name='update_profile'
    ),
    # READ:
    path(
        'account/show/',
        views.DetailProfile.as_view(),
        name='show_profile'
    ),
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
