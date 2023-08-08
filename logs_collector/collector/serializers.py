from rest_framework import serializers

from .models import Archive, Ticket


class ArchiveUploadSerializer(serializers.ModelSerializer):
    ticket_number = serializers.ReadOnlyField(source='ticket.number')

    class Meta:
        model = Archive
        fields = ['file', 'ticket', 'ticket_number']

    def to_internal_value(self, data):
        try:
            ticket = Ticket.objects.get(number=data['ticket'])
            data['ticket'] = ticket.id
            return super().to_internal_value(data)
        except Exception:
            return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ticket'] = data.pop('ticket_number')
        return data
