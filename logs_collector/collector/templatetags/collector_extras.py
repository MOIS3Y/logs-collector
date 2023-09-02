import markdown as md
from django import template
from django.template.defaultfilters import stringfilter

from collector.models import Platform


register = template.Library()


@register.simple_tag()
def get_platforms():
    return Platform.objects.all()


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
