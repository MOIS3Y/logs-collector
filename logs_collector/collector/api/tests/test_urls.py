from django.urls import resolve, reverse
from django.test import TestCase

from collector.api import views


class TestUrls(TestCase):

    def test_list_all_archives_url_is_resolved(self):
        url = reverse('collector_api:archive-list')
        self.assertEquals(resolve(url).func.cls, views.ArchiveViewSet)

    def test_detail_archive_url_is_resolved(self):
        url = reverse('collector_api:archive-detail', args=[1])
        self.assertEquals(resolve(url).func.cls, views.ArchiveViewSet)

    def test_list_all_tickets_url_is_resolved(self):
        url = reverse('collector_api:ticket-list')
        self.assertEquals(resolve(url).func.cls, views.TicketViewSet)

    def test_detail_ticket_url_is_resolved(self):
        url = reverse('collector_api:ticket-detail', args=[1488228])
        self.assertEquals(resolve(url).func.cls, views.TicketViewSet)

    def test_list_all_platforms_url_is_resolved(self):
        url = reverse('collector_api:platform-list')
        self.assertEquals(resolve(url).func.cls, views.PlatformViewSet)

    def test_detail_platform_url_is_resolved(self):
        url = reverse('collector_api:platform-detail', args=['vm6'])
        self.assertEquals(resolve(url).func.cls, views.PlatformViewSet)
