import hashlib
from functools import partial

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import FileField


# Create a custom storage location, using a value from your settings file
sensitive_upload_storage = FileSystemStorage(
    location=settings.MEDIA_ROOT_FOR_SENSITIVE_FILES,
    base_url=settings.MEDIA_URL_FOR_SENSITIVE_FILES
)
# ... and a file field that will use the custom storage
AuthenticatedFileField = partial(FileField, storage=sensitive_upload_storage)


def logs_dir_path(instance, filename):
    # file will be uploaded to
    # MEDIA_ROOT_FOR_SENSITIVE_FILES/<ticket>/<filename>
    return f'{instance.ticket}/{filename}'


class Archive(models.Model):
    file = AuthenticatedFileField(
        upload_to=logs_dir_path,
        blank=True,
        null=True
    )
    sha1 = models.CharField(max_length=1024, editable=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # calculate sha 1 hash sum and write sha1 field to db
        with self.file.open('rb') as f:
            sha1 = hashlib.sha1()
            for byte_block in iter(lambda: f.read(4096), b""):
                sha1.update(byte_block)
            self.sha1 = sha1.hexdigest()
            # Call the "real" save() method
            super().save(*args, **kwargs)

    def __str__(self):
        return str(self.file)


class Platform(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    number = models.IntegerField()
    resolved = models.BooleanField(default=False)
    note = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    platform = models.ForeignKey('Platform', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)
