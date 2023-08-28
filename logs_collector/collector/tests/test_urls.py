from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User

from collector import views
from collector.models import Ticket, Platform


class TestUrls(TestCase):

    def setUp(self):
        # create test user:
        self.test_user = User.objects.create_user(
            username='oops',
            password='hG2wS231YPWmj3'
        )
        # create test platform and ticket:
        self.test_platform = Platform.objects.create(
            name='dci6',
            pretty_name='DCImanager 6'
        )
        self.test_ticket = Ticket.objects.create(
            number=1488228,
            platform=self.test_platform,
            user=self.test_user
        )

    # CREATE:
    def test_ticket_create_url_is_resolved(self):
        url = reverse('collector:create')
        self.assertEquals(resolve(url).func.view_class, views.CreateTicket)

    # READ:
    def test_index_page_url_is_resolved(self):
        url = reverse('collector:index')
        self.assertEquals(resolve(url).func.view_class, views.ListAllTickets)

    def test_list_all_tickets_url_is_resolved(self):
        url = reverse('collector:tickets')
        self.assertEquals(resolve(url).func.view_class, views.ListAllTickets)

    def test_list_platform_tickets_url_is_resolved(self):
        url = reverse('collector:platform', args=[self.test_platform.name])
        self.assertEquals(
            resolve(url).func.view_class, views.ListPlatformTickets
        )

    def test_detail_ticket_url_is_resolved(self):
        url = reverse(
            'collector:ticket',
            args=[self.test_platform.name, self.test_ticket.number]
        )
        self.assertEquals(resolve(url).func.view_class, views.DetailTicket)

    def test_archives_download_url_is_resolved(self):
        url = reverse('collector:download', args=['1488228/test.tar.gz'])
        self.assertEquals(
            resolve(url).func.view_class, views.ArchiveHandlerView
        )

    # UPDATE:
    def test_update_ticket_url_is_resolved(self):
        url = reverse(
            'collector:update',
            args=[self.test_platform.name, self.test_ticket.number]
        )
        self.assertEquals(resolve(url).func.view_class, views.UpdateTicket)
