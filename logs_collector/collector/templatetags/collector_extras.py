import markdown as md
from django import template
from django.template.defaultfilters import stringfilter

from collector.models import Platform


register = template.Library()


@register.simple_tag()
def get_platforms():
    return Platform.objects.all()


@register.filter(name='sizify')
def sizify(value: int) -> str:
    """Simple kb/mb/gb size snippet for templates:

        {{ Archive.file.size|sizify }}

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


@register.filter(name='clean_filename')
def clean_filename(filename: str) -> str:
    """delete prefix ticket number folder for template

    Args:
        filename (str): filename from Filefield

    Returns:
        str: only filename
    """
    return filename.rpartition('/')[-1]


@register.filter(name='markdown')
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])
