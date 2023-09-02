from django.contrib import admin, messages
from django.db.models import F
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ngettext

from .models import Platform, Archive, Ticket
from .utils import sizify


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pretty_name')
    search_fields = ('name',)


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'number',
        'token',
        'platform',
        'user',
        'time_create',
        'time_update',
        'resolved',
    )
    search_fields = ('number',)
    list_filter = ('platform', 'resolved', 'time_create',)
    actions = ['make_resolved', 'make_unresolved']

    @admin.action(description='Mark selected ticket(s) as resolved')
    def make_resolved(self, request, queryset):
        updated = queryset.update(resolved=True)
        self.message_user(
            request,
            ngettext(
                f'{updated} ticket was successfully marked as resolved.',
                f'{updated} tickets were successfully marked as resolved.',
                number=updated,
            ),
            messages.SUCCESS,
        )

    @admin.action(description='Mark selected ticket(s) as unresolved')
    def make_unresolved(self, request, queryset):
        updated = queryset.update(resolved=False)
        self.message_user(
            request,
            ngettext(
                f'{updated} ticket was successfully marked as unresolved.',
                f'{updated} tickets were successfully marked as unresolved.',
                number=updated,
            ),
            messages.SUCCESS,
        )


class ArchiveAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'file_link',
        'file_size',
        'md5',
        'ticket',
        'time_create'
    )
    search_fields = ('ticket',)
    list_filter = ('time_create', 'ticket')

    def get_queryset(self, request):
        qs = super(ArchiveAdmin, self).get_queryset(request)
        qs = qs.annotate(file_size=F('size'))
        return qs

    def file_size(self, obj):
        return sizify(obj.size)

    def file_link(self, obj):
        if obj.file:
            file_name = obj.file.name.rpartition('/')[-1]
            file_path = reverse(
                'collector:download',
                kwargs={'path': obj.file}
            )
            return format_html(
                '<a href="{file_path}">{file_name}</a>',
                file_path=file_path,
                file_name=file_name
            )
        else:
            return "No attachment"

    file_link.allow_tags = True
    file_link.short_description = 'File Download'
    file_size.admin_order_field = 'file_size'


admin.site.register(Platform, PlatformAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Archive, ArchiveAdmin)

admin.site.site_title = 'Logs Collector'
admin.site.site_header = 'LOGS COLLECTOR'
