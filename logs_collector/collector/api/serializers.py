from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from collector.models import Archive, Platform, Ticket


@extend_schema_field(OpenApiTypes.INT)
class TimestampField(serializers.Field):
    def to_representation(self, value) -> int:
        return value.timestamp()


@extend_schema_field(OpenApiTypes.INT)
class JsTimestampField(serializers.Field):
    def to_representation(self, value) -> int:
        return round(value.timestamp()*1000)


class PublicArchiveUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Archive
        fields = ['file', 'ticket']


class ArchiveSerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Archive
        fields = ['id', 'file', 'ticket', 'time_create']


class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = Platform
        fields = ['id', 'name', 'pretty_name']


class TicketSerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    token = serializers.UUIDField(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Ticket
        fields = [
            'id',
            'number',
            'resolved',
            'token',
            'attempts',
            'platform',
            'time_create',
            'time_update',
            'user'
        ]


class StorageInfoSerializer(serializers.Serializer):
    total = serializers.IntegerField(read_only=True)
    used = serializers.IntegerField(read_only=True)
    free = serializers.IntegerField(read_only=True)
    used_percent = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)


class TokenStateRootSerializer(serializers.Serializer):
    info = serializers.CharField(read_only=True, default="manual message")


class TokenStateSerializer(serializers.ModelSerializer):
    token = serializers.UUIDField(read_only=True)
    attempts = serializers.IntegerField(read_only=True)
    resolved = serializers.BooleanField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'token',
            'attempts',
            'resolved'
        ]


class AppHealthInfoSerializer(serializers.Serializer):
    status = serializers.CharField(read_only=True, default="ok")
