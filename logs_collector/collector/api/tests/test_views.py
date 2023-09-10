from pathlib import Path
from django.core.files.base import ContentFile
from django.conf import settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User

from collector.models import Archive, Platform, Ticket


def delete_test_files(ticket):
    test_file = settings.MEDIA_ROOT / Path(str(ticket))
    test_file.unlink(missing_ok=True)


class TestViews(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create(
            username='oops',
            password='hG2wS231YPWmj3'
        )
        self.test_platform = Platform.objects.create(
            name='vm6',
            pretty_name='VMmanager 6'
        )
        self.test_ticket = Ticket.objects.create(
            number=1488228,
            platform=self.test_platform,
            token='e04f4c3c-ef80-49ee-a2c3-89b737a67cdb',
            user=self.test_user
        )
        self.archive_list_url = reverse('collector_api:archive-list')
        self.test_file = ContentFile(b'...', name='test.tar.gz')
        self.test_upload_data = {'file': self.test_file}

    def test_success_upload_file_from_anon_user(self):
        response = self.client.post(
            self.archive_list_url,
            self.test_upload_data,
            format='multipart',
            headers={'Upload-Token': self.test_ticket.token}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_archive = Archive.objects.last()
        # ? workaround delete test file:
        delete_test_files(test_archive.file)

    def test_deny_401_upload_file_from_anon_user(self):
        response = self.client.post(
            self.archive_list_url,
            self.test_upload_data,
            format='multipart',
            # missing header: Upload-Token
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deny_403_wrong_token_upload_file_from_anon_user(self):
        response = self.client.post(
            self.archive_list_url,
            self.test_upload_data,
            format='multipart',
            headers={'Upload-Token': 'wrong-token'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_423_expired_token_upload_file_from_anon_user(self):
        # attribute overload (expired):
        self.test_ticket.attempts = 0
        self.test_ticket.save()
        response = self.client.post(
            self.archive_list_url,
            self.test_upload_data,
            format='multipart',
            headers={'Upload-Token': self.test_ticket.token}
        )
        self.assertEqual(response.status_code, status.HTTP_423_LOCKED)

    def test_deny_423_resolved_ticket_state_upload_file_from_anon_user(self):
        # attribute overload (ticket resolved):
        self.test_ticket.resolved = True
        self.test_ticket.save()
        response = self.client.post(
            self.archive_list_url,
            self.test_upload_data,
            format='multipart',
            headers={'Upload-Token': self.test_ticket.token}
        )
        self.assertEqual(response.status_code, status.HTTP_423_LOCKED)

    def test_deny_archive_list_GET_method_for_anon_user(self):
        response = self.client.get(self.archive_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deny_archive_list_PUT_method_for_anon_user(self):
        response = self.client.put(
            self.archive_list_url,
            self.test_upload_data,
            format='multipart',
            headers={'Upload-Token': self.test_ticket.token}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deny_archive_list_DELETE_method_for_anon_user(self):
        response = self.client.delete(
            reverse('collector_api:archive-list'),
            data={'id': 1},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
