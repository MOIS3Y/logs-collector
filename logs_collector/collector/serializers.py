from rest_framework import serializers

from .models import Archive, Ticket


class ArchiveUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Archive
        fields = ['file', 'ticket']


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['number', 'platform', 'note']
