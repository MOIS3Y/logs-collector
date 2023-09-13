from rest_framework import permissions


class IsGuestUpload(permissions.BasePermission):
    """
    Special permission class for the ability to upload attachments
    to an unauthorized user using a ticket token
    """
    def has_permission(self, request, view):
        if request.method in ('HEAD', 'OPTIONS', 'POST',):
            return True

        return request.user.is_authenticated


class IsGuestCheckUrls(permissions.BasePermission):
    """
    Special permission class for the ability to upload attachments
    to an unauthorized user using a ticket token
    """
    def has_permission(self, request, view):
        if request.method in ('HEAD', 'OPTIONS', 'GET',):
            return True

        return request.user.is_authenticated
