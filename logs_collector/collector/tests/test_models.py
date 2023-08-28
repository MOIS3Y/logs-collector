from pathlib import Path
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.conf import settings

from collector.models import Platform, Ticket, Archive


def delete_test_files(ticket):
    test_file = settings.MEDIA_ROOT_FOR_SENSITIVE_FILES / Path(str(ticket))
    test_file.unlink(missing_ok=True)


class TestModels(TestCase):

    def setUp(self):
        # create test user:
        self.test_user = User.objects.create_user(
            username='oops',
            password='hG2wS231YPWmj3'
        )
        # create test platform and ticket:
        self.test_platform = Platform.objects.create(
            name='vm6',
            pretty_name='VMmanager 6'
        )
        self.test_ticket = Ticket.objects.create(
            number=1488228,
            platform=self.test_platform,
            user=self.test_user
        )

    def test_correct_platform_fields(self):
        self.assertEqual(self.test_platform.name, 'vm6')
        self.assertEqual(self.test_platform.pretty_name, 'VMmanager 6')

    def test_correct_ticket_fields(self):
        self.assertEqual(self.test_ticket.number, 1488228)
        self.assertEqual(self.test_ticket.attempts, 5)
        self.assertEqual(
            self.test_ticket.platform.name,
            self.test_platform.name
        )

    def test_correct_archive_fields(self):
        test_archive = Archive.objects.create(
            file=ContentFile(b'...', name='test.tar.gz'),
            ticket=self.test_ticket
        )
        triple_dots_md5 = '2f43b42fd833d1e77420a8dae7419000'
        self.assertEquals(test_archive.md5, triple_dots_md5)
        self.assertEquals(
            test_archive.file.name,
            f'{self.test_ticket.number}/test.tar.gz'
        )
        # ? workaround delete test file:
        delete_test_files(test_archive.file)
