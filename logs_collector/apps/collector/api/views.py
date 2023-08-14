from django.core.exceptions import ValidationError, ObjectDoesNotExist

from rest_framework import status
# from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from apps.collector.models import Archive, Ticket, Platform  # ???????

from .filters import ArchiveFilter, TicketFilter
from .permissions import IsGuestUpload
from .serializers import (
    PublicArchiveUploadSerializer,
    ArchiveSerializer,
    PlatformSerializer,
    TicketSerializer
)


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
