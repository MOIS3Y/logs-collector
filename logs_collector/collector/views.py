import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, JsonResponse
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy

from rest_framework import status
# from rest_framework.response import Response

from .models import Archive, Ticket, Platform
from .utils import is_ajax


class ArchiveHandlerView(LoginRequiredMixin, SingleObjectMixin, generic.View):
    model = Archive
    slug_field = 'file'
    slug_url_kwarg = 'path'

    def get(self, request, path):
        self.object = self.get_object()
        return FileResponse(self.object.file)

    def delete(self, request, path):
        if is_ajax(request):
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'file': path}, status=status.HTTP_200_OK)


class ListAllTickets(generic.ListView):
    model = Ticket
    template_name = 'collector/tickets.html'
    context_object_name = 'tickets'
    paginate_by = 5

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['platforms'] = Platform.objects.all()
    #     return context


class ListPlatformTickets(generic.ListView):
    model = Ticket
    template_name = 'collector/tickets.html'
    context_object_name = 'tickets'
    # allow_empty = False
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


class UpdateTicketStateHandler(SingleObjectMixin, generic.View):
    model = Ticket
    slug_field = 'number'
    slug_url_kwarg = 'ticket'

    def post(self, request, **kwargs):
        if is_ajax(request):
            self.object = self.get_object()
            if request.body:
                data = json.loads(request.body)
                resolved_field = data.get('resolved')
                if isinstance(resolved_field, bool):
                    self.object.resolved = not resolved_field
                    self.object.save()
                    return JsonResponse(
                        {'resolved': not resolved_field},
                        status=status.HTTP_201_CREATED
                    )
                return JsonResponse(
                    {'resolved': 'must be a boolean'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return JsonResponse(
            {'error': 'header XMLHttpRequest is required'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )


class DeleteTicketHandler(SingleObjectMixin, generic.View):
    model = Ticket
    slug_field = 'number'
    slug_url_kwarg = 'ticket'

    def delete(self, request, ticket):
        if is_ajax(request):
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse(
                {'status': status.HTTP_200_OK},
                status=status.HTTP_200_OK
            )
        return JsonResponse(
            {'error': 'header XMLHttpRequest is required'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
