from rest_framework import serializers

from .models import Archive, Platform, Ticket


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return value.timestamp()


class JsTimestampField(serializers.Field):
    def to_representation(self, value):
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

    def to_representation(self, instance):
        print(int(round(instance.time_create.timestamp())))
        return super().to_representation(instance)


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
