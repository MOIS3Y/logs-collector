from rest_framework import serializers

from .models import Archive


class ArchiveUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Archive
        fields = ['file', 'ticket']
