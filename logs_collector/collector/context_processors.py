from django.conf import settings

from . import __author__
from .utils.helpers import get_mount_fs_info


def metadata(request):
    return {
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "author": __author__,
    }


def storage_info(request):
    return {'storage': get_mount_fs_info(settings.MEDIA_ROOT)}
