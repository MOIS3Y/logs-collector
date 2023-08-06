import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, JsonResponse
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy

from rest_framework import status
# from rest_framework.response import Response

from .models import Archive, Ticket
from .forms import TicketForm
from .utils import PageTitleViewMixin, is_ajax


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


class CreateTicket(LoginRequiredMixin, PageTitleViewMixin, generic.CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'collector/ticket_create.html'

    def get_title(self):
        return f'{self.title} - create'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateTicket(LoginRequiredMixin, PageTitleViewMixin, generic.UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'collector/ticket_create.html'
    slug_field = 'number'
    slug_url_kwarg = 'ticket'

    def get_title(self, **kwargs):
        return f'{self.title} - {self.kwargs.get("ticket", "update")}'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ListAllTickets(PageTitleViewMixin, generic.ListView):
    model = Ticket
    template_name = 'collector/tickets.html'
    context_object_name = 'tickets'
    paginate_by = 5
    title = 'Collector - tickets'


class ListPlatformTickets(PageTitleViewMixin, generic.ListView):
    model = Ticket
    template_name = 'collector/tickets.html'
    context_object_name = 'tickets'
    # allow_empty = False
    paginate_by = 5

    def get_title(self, **kwargs):
        return f'{self.title} - {self.kwargs.get("platform", "tickets")}'

    def get_queryset(self):
        return Ticket.objects.filter(
            platform__name=self.kwargs.get('platform')
        )


class DetailTicket(PageTitleViewMixin, generic.DetailView):
    model = Ticket
    template_name = 'collector/ticket.html'
    context_object_name = 'ticket'
    slug_field = 'number'
    slug_url_kwarg = 'ticket'

    def get_title(self, **kwargs):
        return f'{self.title} - {self.kwargs.get("ticket", "show")}'


class DeleteTicket(PageTitleViewMixin, generic.DeleteView):
    model = Ticket
    template_name = 'collector/ticket_delete.html'
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
