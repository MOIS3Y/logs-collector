from django.contrib import admin

from .models import Platform, Archive, Ticket


# Register your models here.
class PlatformAdmin(admin.ModelAdmin):
    pass


class TicketAdmin(admin.ModelAdmin):
    pass


class ArchiveAdmin(admin.ModelAdmin):
    pass


admin.site.register(Platform, PlatformAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Archive, ArchiveAdmin)
