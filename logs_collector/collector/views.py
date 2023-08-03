import json
# from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponseNotAllowed, JsonResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from rest_framework import status
# from rest_framework.response import Response

from .models import Archive, Ticket, Platform
from .utils import is_ajax


class ArchiveHandlerView(LoginRequiredMixin, generic.View):
    def get(self, request, path):
        file = get_object_or_404(Archive, file=path)
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
    slug_field = 'number'
    slug_url_kwarg = 'ticket'

    def post(self, request, **kwargs):
        if is_ajax(request):
            model = self.get_object()
            if request.body:
                data = json.loads(request.body)
                resolved_field = data.get('resolved')
                if isinstance(resolved_field, bool):
                    model.resolved = not resolved_field
                    model.save()
                    return JsonResponse(
                        {'resolved': not resolved_field},
                        status=status.HTTP_201_CREATED
                    )
                return JsonResponse(
                    {'resolved': 'must be a boolean'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return HttpResponseNotAllowed(permitted_methods=['GET'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platforms'] = Platform.objects.all()
        return context


class DeleteTicket(generic.DeleteView):
    model = Ticket
    template_name = 'collector/delete_ticket.html'
    context_object_name = 'ticket'
    slug_field = 'number'
    slug_url_kwarg = 'ticket'
    success_url = reverse_lazy('tickets')

    def delete(self, request, *args, **kwargs):
        if is_ajax(request):
            print("HELLO FROM AJAX")
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse(
                {'status': status.HTTP_200_OK},
                status=status.HTTP_200_OK
            )
        response = super().delete(self, request, *args, **kwargs)
        return response


class AjaxDeleteTicketHandler(generic.View):

    def delete(self, request, ticket):
        if is_ajax(request):
            print("HELLO FROM AJAX")
            obj = Ticket.objects.get(number=ticket)
            obj.delete()
            return JsonResponse(
                {'status': status.HTTP_200_OK},
                status=status.HTTP_200_OK
            )
