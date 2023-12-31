from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q

from two_factor.views import OTPRequiredMixin

from .forms import TicketForm, ArchiveForm
from .models import Archive, Ticket
from .utils.mixins import ExtraContextMixin


class ArchiveUploadView(ExtraContextMixin, generic.TemplateView):
    form_class = ArchiveForm()
    template_name = 'collector/archive_upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def get_title(self):
        return f'{self.title} - upload'


class ArchiveHandlerView(
        OTPRequiredMixin,
        LoginRequiredMixin,
        SingleObjectMixin,
        generic.View):
    model = Archive
    slug_field = 'file'
    slug_url_kwarg = 'path'

    def get(self, request, path):
        self.object = self.get_object()
        try:
            self.object.file.size
        except FileNotFoundError:
            raise Http404(f'File: {self.object.file} not found')
        return FileResponse(self.object.file)


class CreateTicket(LoginRequiredMixin, ExtraContextMixin, generic.CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'collector/ticket_create.html'

    def get_title(self):
        return f'{self.title} - create'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateTicket(LoginRequiredMixin, ExtraContextMixin, generic.UpdateView):
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


class ListAllTickets(LoginRequiredMixin, ExtraContextMixin, generic.ListView):
    model = Ticket
    template_name = 'collector/tickets.html'
    context_object_name = 'tickets'
    paginate_by = 5
    title = 'Collector - tickets'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        resolved_status_query = self.request.GET.get('resolved', '')
        if search_query or resolved_status_query:
            self.paginate_by = 100  # ? fake disable pagination)
            if search_query:
                query_list = []
                try:
                    for item in search_query.split(','):
                        query_list.append(int(item))
                except ValueError:
                    return super().get_queryset()
                queryset = self.model.objects.filter(
                    Q(number__in=query_list) | Q(number__icontains=query_list[0])  # noqa:E501
                )
            if resolved_status_query:
                queryset = self.model.objects.filter(Q(resolved=True))
            return queryset

        return super().get_queryset()


class ListPlatformTickets(LoginRequiredMixin, ExtraContextMixin, generic.ListView):  # noqa:E501
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


class DetailTicket(LoginRequiredMixin, ExtraContextMixin, generic.DetailView):
    model = Ticket
    template_name = 'collector/ticket.html'
    context_object_name = 'ticket'
    slug_field = 'number'
    slug_url_kwarg = 'ticket'

    def get_title(self, **kwargs):
        return f'{self.title} - {self.kwargs.get("ticket", "show")}'
