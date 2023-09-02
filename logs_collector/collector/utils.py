def logs_dir_path(instance, filename):
    """
        file will be uploaded to
        MEDIA_ROOT_FOR_SENSITIVE_FILES/<ticket-token>/<filename>
    """
    return f'{instance.ticket.number}/{filename}'


def sizify(value: int) -> str:
    """Simple kb/mb/gb size snippet for admin panel custom field:

    Args:
        value (int): size of file from Filefield

    Returns:
        str: format human readable size like 4.2 Gb
    """
    if value < 512000:
        value = value / 1024.0
        ext = 'Kb'
    elif value < 4194304000:
        value = value / 1048576.0
        ext = 'Mb'
    else:
        value = value / 1073741824.0
        ext = 'Gb'
    return f'{round(value, 2)} {ext}'


class PageTitleViewMixin:
    title = 'Collector'

    def get_title(self, *args, **kwargs):
        """
        Return the class title attr by default,
        but you can override this method to further customize
        """
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context
