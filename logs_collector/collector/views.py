import json
# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, JsonResponse, Http404
from django.views import generic

from rest_framework import status
# from rest_framework.response import Response

from .models import Archive, Ticket, Platform
from .utils import is_ajax


class ArchiveHandlerView(LoginRequiredMixin, generic.View):
    def get(self, request, path):
        try:
            file = Archive.objects.get(file=path)
        except Archive.DoesNotExist:
            return Http404
        return FileResponse(file.file)

    def delete(self, request, path):
        try:
            file = Archive.objects.get(file=path)
            file.delete()
            return JsonResponse(
                {
                    'file': path,
                    'status': status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        except Archive.DoesNotExist:
            return JsonResponse(
                {
                    'file': path,
                    'status': status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_204_NO_CONTENT
            )


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

    def post(self, request, platform, ticket):
        if is_ajax(request):
            model = self.get_object()
            if request.body:
                data = json.loads(request.body)
                if data.get('resolved') is True:
                    model.resolved = False
                    model.save()
                if data.get('resolved') is False:
                    model.resolved = True
                    model.save()
        return JsonResponse({'status': 201}, status=status.HTTP_201_CREATED)

    def get_object(self, queryset=None):
        return self.model.objects.get(number=self.kwargs.get('ticket'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platforms'] = Platform.objects.all()
        return context
