# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.views import generic

from rest_framework import status
from rest_framework.response import Response

from .models import Archive, Ticket, Platform


# handles the url "/archives/{PATH}"".
@login_required
def download(request, path):
    try:
        file = Archive.objects.get(file=path)
    except Archive.DoesNotExist:
        return Http404

    return FileResponse(file.file)


class ArchiveHandlerView(generic.View):
    def get(self, request, path):
        try:
            file = Archive.objects.get(file=path)
        except Archive.DoesNotExist:
            return Http404
        return FileResponse(file.file)

    def delete(self, request, path):
        content = {'file': path}
        try:
            file = Archive.objects.get(file=path)
            file.delete()
            return Response(content, status=status.HTTP_200_OK)
        except Archive.DoesNot.Exist:
            return Response(content, status=status.HTTP_204_NO_CONTENT)


class ListAllTickets(generic.ListView):
    model = Ticket
    template_name = 'collector/tickets.html'
    context_object_name = 'tickets'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platforms'] = Platform.objects.all()
        return context


class ListPlatformTickets(generic.ListView):
    model = Ticket
    template_name = 'collector/tickets.html'
    context_object_name = 'tickets'
    allow_empty = False
    paginate_by = 5

    def get_queryset(self):
        return Ticket.objects.filter(
            platform__name=self.kwargs.get('platform')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platforms'] = Platform.objects.all()
        return context


class DetailTicket(generic.DetailView):
    model = Ticket
    template_name = 'collector/ticket.html'
    context_object_name = 'ticket'

    def get_object(self, queryset=None):
        return Ticket.objects.get(number=self.kwargs.get('ticket'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platforms'] = Platform.objects.all()
        return context
