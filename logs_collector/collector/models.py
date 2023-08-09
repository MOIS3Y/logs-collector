import uuid
import hashlib
from functools import partial

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

from .utils import logs_dir_path


# Create a custom storage location, using a value from your settings file
sensitive_upload_storage = FileSystemStorage(
    location=settings.MEDIA_ROOT_FOR_SENSITIVE_FILES,
    base_url=settings.MEDIA_URL_FOR_SENSITIVE_FILES
)
# ... and a file field that will use the custom storage
AuthenticatedFileField = partial(
    models.FileField,
    storage=sensitive_upload_storage
)


class Archive(models.Model):
    file = AuthenticatedFileField(
        upload_to=logs_dir_path,
        blank=True,
        null=True
    )
    md5 = models.CharField(max_length=1024, editable=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(
        'Ticket',
        to_field='number',
        db_column='ticket_number',
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        # calculate sha 1 hash sum and write md5 field to db
        with self.file.open('rb') as f:
            md5 = hashlib.md5()
            for byte_block in iter(lambda: f.read(4096), b""):
                md5.update(byte_block)
            self.md5 = md5.hexdigest()
            # Call the "real" save() method
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('collector:download', kwargs={'path': self.file})

    def __str__(self):
        return str(self.file)


class Platform(models.Model):
    name = models.CharField(max_length=20, unique=True)
    pretty_name = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('collector:platform', kwargs={'platform': self.name})

    def __str__(self):
        return self.pretty_name


class Ticket(models.Model):
    number = models.IntegerField(unique=True, db_index=True)
    resolved = models.BooleanField(default=False)
    note = models.TextField(blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    attempts = models.IntegerField(default=5, validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    platform = models.ForeignKey(
        'Platform',
        to_field='name',
        db_column='platform_name',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-time_create']

    def get_absolute_url(self):
        return reverse(
            'collector:ticket',
            kwargs={'platform': self.platform.name, 'ticket': self.number}
        )

    def __str__(self):
        return str(self.number)
