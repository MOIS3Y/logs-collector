from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView
)

from account import views


class TestUrls(TestCase):

    # READ:
    def test_account_logout_url_is_resolved(self):
        url = reverse('account:logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_account_show_url_is_resolved(self):
        url = reverse('account:show_profile')
        self.assertEquals(resolve(url).func.view_class, views.DetailProfile)

    def test_password_change_done_url_is_resolved(self):
        url = reverse('account:password_change_done')
        self.assertEquals(
            resolve(url).func.view_class, PasswordChangeDoneView
        )

    # UPDATE:
    def test_password_change_url_is_resolved(self):
        url = reverse('account:password_change')
        self.assertEquals(resolve(url).func.view_class, PasswordChangeView)

    def test_account_update_url_is_resolved(self):
        url = reverse('account:update_profile')
        self.assertEquals(resolve(url).func.view_class, views.UpdateProfile)
