from django.conf import settings

from .utils.helpers import get_mount_fs_info


def metadata(request):
    return {
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


def storage_info(request):
    return get_mount_fs_info(settings.MEDIA_ROOT)
