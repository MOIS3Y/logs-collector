from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from collector.models import Archive, Platform, Ticket


@extend_schema_field(OpenApiTypes.NUMBER)
class TimestampField(serializers.Field):
    def to_representation(self, value) -> int:
        return value.timestamp()


@extend_schema_field(OpenApiTypes.NUMBER)
class JsTimestampField(serializers.Field):
    def to_representation(self, value) -> int:
        return round(value.timestamp()*1000)


class PublicArchiveUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = ['file', 'ticket']


class ArchiveSerializer(serializers.ModelSerializer):
    time_create = JsTimestampField(read_only=True)

    class Meta:
        model = Archive
        fields = ['id', 'file', 'ticket', 'time_create']


class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = Platform
        fields = ['id', 'name', 'pretty_name']


class TicketSerializer(serializers.ModelSerializer):
    time_create = JsTimestampField(read_only=True)
    time_update = JsTimestampField(read_only=True)
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