from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings

from rest_framework import status
# from rest_framework.decorators import action
from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
    FileUploadParser
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters, generics, views, viewsets

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.openapi import OpenApiParameter

from collector.models import Archive, Ticket, Platform
from collector.utils.helpers import get_mount_fs_info

from .filters import ArchiveFilter, TicketFilter
from .permissions import IsGuestUpload, IsGuestCheckUrls
from .serializers import (
    PublicArchiveUploadSerializer,
    ArchiveSerializer,
    PlatformSerializer,
    TicketSerializer,
    StorageInfoSerializer,
    TokenStateSerializer,
    AppHealthInfoSerializer,
    TokenStateRootSerializer,
)


@extend_schema_view(
    list=extend_schema(
        description='Archives that contains log files for checking',
        summary='Show all archives'
    ),
    create=extend_schema(summary='Create (upload) a new archive'),
    retrieve=extend_schema(summary='Show archive by id'),
    update=extend_schema(summary='Update archive'),
    partial_update=extend_schema(summary='Update archive field'),
    destroy=extend_schema(summary='Delete archive'),
)
class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.order_by('-time_create')
    serializer_class = ArchiveSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    permission_classes = (IsGuestUpload, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArchiveFilter

    @extend_schema(
        operation_id='upload_file',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                        }
                    }
                }
            },
        parameters=[
            OpenApiParameter(
                name='Upload-Token',
                type=str,
                location=OpenApiParameter.HEADER,
                description="upload permission token",
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        # ! upload-token protection:
        upload_token = request.headers.get('upload-token', '')
        if upload_token:
            try:
                bound_ticket = Ticket.objects.get(token=upload_token)
                if bound_ticket.resolved:
                    return Response(
                        {'detail': f'ticket {bound_ticket} already resolved'},
                        status=status.HTTP_423_LOCKED
                    )
                if bound_ticket.attempts <= 0:
                    return Response(
                        {'detail': f'token {upload_token} expired'},
                        status=status.HTTP_423_LOCKED
                    )
                bound_ticket.attempts -= 1
                bound_ticket.save()
                # ? mixin bound ticket number to request.data from user
                try:
                    request.data['ticket'] = bound_ticket.number
                except AttributeError:
                    return Response(
                        {'detail': 'Bad Request'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # ? change serializer for guest user
                if not request.user.is_authenticated:
                    self.serializer_class = PublicArchiveUploadSerializer
            except (ValidationError, ObjectDoesNotExist,):
                return Response(
                    {'detail': f'token {upload_token} is not valid'},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {'detail': 'Header Upload-Token is required'},
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


@extend_schema_view(
    list=extend_schema(
        description='Platforms are needed to relative the ticket and software',
        summary='Show all platforms'
    ),
    create=extend_schema(summary='Create a new platform'),
    retrieve=extend_schema(summary='Show platform by internal name'),
    update=extend_schema(summary='Update platform'),
    partial_update=extend_schema(summary='Update platform field'),
    destroy=extend_schema(summary='Delete platform'),
)
class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    lookup_field = 'name'
    serializer_class = PlatformSerializer
    permission_classes = (IsAuthenticated, )


@extend_schema_view(
    list=extend_schema(
        description='Tickets that will be related with the uploaded archive',
        summary='Show all tickets'
    ),
    create=extend_schema(summary='Create a new ticket'),
    retrieve=extend_schema(summary='Show ticket by number'),
    update=extend_schema(summary='Update ticket'),
    partial_update=extend_schema(summary='Update ticket field'),
    destroy=extend_schema(summary='Delete ticket'),
)
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


class StorageInfo(views.APIView):
    """Info about storage total/used/free space"""

    permission_classes = (IsAuthenticated, )

    @extend_schema(
        responses=StorageInfoSerializer,
        summary='Show storage space in bytes'
    )
    def get(self, request):
        return Response(get_mount_fs_info(settings.DATA_DIR))


class TokenStateRoot(views.APIView):
    """ Show the message of a specific upload token URL"""
    permission_classes = (IsGuestCheckUrls,)

    @extend_schema(
        responses=TokenStateRootSerializer,
        summary='Show info message how get token status'
    )
    def get(self, request):
        message = "to find out the status of the token, place it in the URL"
        return Response({"detail": message}, status=status.HTTP_303_SEE_OTHER)


@extend_schema_view(
    get=extend_schema(
        summary='Show the status of a specific upload token'
    )
)
class TokenStateInfo(generics.RetrieveAPIView):
    """ Show the status of a specific upload token"""
    queryset = Ticket.objects.order_by('-time_create')
    lookup_field = 'token'
    serializer_class = TokenStateSerializer
    permission_classes = (IsGuestCheckUrls,)


class AppHealthInfo(views.APIView):
    permission_classes = (IsGuestCheckUrls,)

    @extend_schema(
        responses=AppHealthInfoSerializer,
        summary='Show app status'
    )
    def get(self, request):
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
