from django.contrib import admin
from .models import Invite, Guest


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('name', 'dietary_restrictions', 'is_attending',)


class InviteAdmin(admin.ModelAdmin):
    inlines = [GuestInline]
    list_display = ("family_name", "finished", "invite_url", "email",)
    exclude = ("invite_url", "finished",)
    view_on_site = True


# Register your models here.
admin.site.register(Invite, InviteAdmin)
