from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q

from rest_framework import status
# from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from two_factor.views import OTPRequiredMixin

from .models import Archive, Ticket, Platform
from .forms import TicketForm
from .filters import ArchiveFilter, TicketFilter
from .utils import PageTitleViewMixin
from .permissions import IsGuestUpload

from .serializers import (
    PublicArchiveUploadSerializer,
    ArchiveSerializer,
    PlatformSerializer,
    TicketSerializer
)


class ArchiveHandlerView(
        OTPRequiredMixin,
        LoginRequiredMixin,
        SingleObjectMixin,
        generic.View):
    model = Archive
    slug_field = 'file'
    slug_url_kwarg = 'path'

    def get(self, request, path):
        self.object = self.get_object()
        return FileResponse(self.object.file)


class CreateTicket(LoginRequiredMixin, PageTitleViewMixin, generic.CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'collector/ticket_create.html'

    def get_title(self):
        return f'{self.title} - create'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateTicket(LoginRequiredMixin, PageTitleViewMixin, generic.UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'collector/ticket_create.html'
    slug_field = 'number'
    slug_url_kwarg = 'ticket'

    def get_title(self, **kwargs):
        return f'{self.title} - {self.kwargs.get("ticket", "update")}'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ListAllTickets(LoginRequiredMixin, PageTitleViewMixin, generic.ListView):
    model = Ticket
    template_name = 'collector/tickets.html'
    context_object_name = 'tickets'
    paginate_by = 5
    title = 'Collector - tickets'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            query_list = []
            try:
                for item in search_query.split(','):
                    query_list.append(int(item))
            except ValueError:
                return super().get_queryset()
            queryset = self.model.objects.filter(
                Q(number__in=query_list) | Q(number__icontains=query_list[0])
            )
            self.paginate_by = 100  # ? fake disable pagination)
            return queryset

        return super().get_queryset()


class ListPlatformTickets(
        LoginRequiredMixin,
        PageTitleViewMixin,
        generic.ListView
        ):
    model = Ticket
    template_name = 'collector/tickets.html'
    context_object_name = 'tickets'
    # allow_empty = False
    paginate_by = 5

    def get_title(self, **kwargs):
        return f'{self.title} - {self.kwargs.get("platform", "tickets")}'

    def get_queryset(self):
        return Ticket.objects.filter(
            platform__name=self.kwargs.get('platform')
        )


class DetailTicket(LoginRequiredMixin, PageTitleViewMixin, generic.DetailView):
    model = Ticket
    template_name = 'collector/ticket.html'
    context_object_name = 'ticket'
    slug_field = 'number'
    slug_url_kwarg = 'ticket'

    def get_title(self, **kwargs):
        return f'{self.title} - {self.kwargs.get("ticket", "show")}'


class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.order_by('-time_create')
    serializer_class = ArchiveSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsGuestUpload, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArchiveFilter

    def create(self, request, *args, **kwargs):
        # ! upload-token protection:
        upload_token = request.headers.get('upload-token', '')
        if not request.user.is_authenticated and upload_token:
            try:
                bound_ticket = Ticket.objects.get(token=upload_token)
                if bound_ticket.resolved:
                    return Response(
                        {'error': f'ticket {upload_token} already resolved'},
                        status=status.HTTP_423_LOCKED
                    )
                if bound_ticket.attempts <= 0:
                    return Response(
                        {'error': f'token {upload_token} expired'},
                        status=status.HTTP_423_LOCKED
                    )
                bound_ticket.attempts -= 1
                bound_ticket.save()
                # ? mixin bound ticket number to request.data from user
                request.data['ticket'] = bound_ticket.number
                # ? change serializer for guest user
                self.serializer_class = PublicArchiveUploadSerializer
            except (ValidationError, ObjectDoesNotExist,):
                return Response(
                    {'error': f'token {upload_token} is not valid'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif not request.user.is_authenticated:
            return Response(
                {'error': 'Header Upload-Token is required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        # ! default create method:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    lookup_field = 'name'
    serializer_class = PlatformSerializer
    permission_classes = (IsAuthenticated, )


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.order_by('-time_create')
    lookup_field = 'number'
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TicketFilter
    search_fields = ['number']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
