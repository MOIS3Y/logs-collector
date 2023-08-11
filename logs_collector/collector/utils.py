import os


def logs_dir_path(instance, filename):
    # file will be uploaded to
    # MEDIA_ROOT_FOR_SENSITIVE_FILES/<ticket-token>/<filename>
    return f'{instance.ticket.number}/{filename}'


def get_file_size(file_path, unit='bytes'):
    file_size = os.path.getsize(file_path)
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)


def is_ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True


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
