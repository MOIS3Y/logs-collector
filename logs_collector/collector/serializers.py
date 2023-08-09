from rest_framework import serializers

from .models import Archive


class PublicArchiveUploadSerializer(serializers.ModelSerializer):
    ticket = serializers.ReadOnlyField(source='ticket.token')

    class Meta:
        model = Archive
        fields = ['file', 'ticket']
