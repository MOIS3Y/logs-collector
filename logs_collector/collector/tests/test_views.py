from django.test import TestCase, Client
from django.urls import reverse

from account.models import User

from collector.models import Ticket, Platform


class TestViews(TestCase):

    def setUp(self):
        # create test user:
        self.test_user = User.objects.create_user(
            username='oops',
            password='hG2wS231YPWmj3'
        )
        # create test client:
        self.client = Client()
        self.client.login(username='oops', password='hG2wS231YPWmj3')
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

        # test urls:
        # -- -- -- --

        # CREATE:
        self.ticket_create_url = reverse('collector:create')

        # READ:
        self.all_tickets_list = reverse('collector:tickets')
        self.platform_tickets_list = reverse(
            'collector:platform',
            args=[self.test_platform.name]
        )
        self.ticket_detail_url = reverse(
            'collector:ticket',
            args=[self.test_platform.name, self.test_ticket.number]
        )

        # UPDATE:
        self.ticket_update_url = reverse(
            'collector:update',
            args=[self.test_platform.name, self.test_ticket.number]
        )

    # CREATE:
    def test_create_ticket_POST(self):
        response = self.client.post(
            self.ticket_create_url,
            data={
                'number': 1111,
                'platform': self.test_platform.name,
                'attempts': 5
            }
        )
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Ticket.objects.get(number=1111).number, 1111)
        self.assertEquals(Ticket.objects.get(number=1111).platform.name, 'vm6')
        self.assertEquals(
            Ticket.objects.get(
                number=1111).platform.pretty_name, 'VMmanager 6'
            )
        self.assertEquals(
            Ticket.objects.get(number=1111).user.username, 'oops'
        )

    # READ:
    def test_all_ticket_list_GET(self):
        response = self.client.get(self.all_tickets_list)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'collector/tickets.html')
        self.assertTemplateUsed(response, 'collector/base.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'includes/theme_switcher.html')
        self.assertTemplateUsed(response, 'includes/navigation.html')
        self.assertTemplateUsed(response, 'collector/includes/pagination.html')
        self.assertTemplateUsed(
            response,
            'collector/includes/ticket_info.html'
        )
        self.assertTemplateUsed(
            response,
            'collector/includes/modal_ticket.html'
        )

    def test_platform_tickets_list_GET(self):
        response = self.client.get(self.platform_tickets_list)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'collector/tickets.html')

    def test_ticket_detail_GET(self):
        response = self.client.get(self.ticket_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'collector/ticket.html')
        self.assertTemplateUsed(
            response, 'collector/includes/ticket_info.html'
        )
        self.assertTemplateUsed(
            response, 'collector/includes/modal_ticket.html'
        )

    def test_ticket_create_GET(self):
        response = self.client.get(self.ticket_create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'collector/ticket_create.html')

    def test_ticket_update_GET(self):
        response = self.client.get(self.ticket_update_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'collector/ticket_create.html')

    # UPDATE:
    def test_ticket_update_UPDATE(self):
        response = self.client.post(
            self.ticket_update_url,
            data={
                'number': 1488229,
                'platform': self.test_platform.name,
                'attempts': 3
            }
        )
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Ticket.objects.get(number=1488229).number, 1488229)
        self.assertEquals(Ticket.objects.get(number=1488229).attempts, 3)
