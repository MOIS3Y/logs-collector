# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, Http404
from .models import Archive


# Create your views here.
# handles the url "/archives/{PATH}"".
@login_required
def download(request, ticket, file):
    path = f'{ticket}/{file}'
    try:
        file = Archive.objects.get(file=path)
    except Archive.DoesNotExist:
        return Http404

    return FileResponse(file.file)


def index(request):
    return HttpResponse('<h1>Index Page</h1>')


def test_page(request, path):
    return HttpResponse(f'<h1>{path} Page</h1>')
