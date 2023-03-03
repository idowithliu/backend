from django.contrib import admin
from .models import Invite, Guest, Email
from registry.models import FundContrib
# from registry.models import Fund


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('name', 'dietary_restrictions', 'is_attending',)

class EmailInline(admin.TabularInline):
    model = Email
    fields = ('address',)

class FundContribInline(admin.TabularInline):
    model = FundContrib
    fields = ('amount', 'fund',)


# class FundsInline(admin.TabularInline):
#     model = Fund
#     fields = ('amount',)


class InviteAdmin(admin.ModelAdmin):
    inlines = [EmailInline, GuestInline, FundContribInline]
    list_display = ("family_name", "finished", "invite_url",)
    exclude = ("invite_url", "finished", 'pseudo_id',)
    view_on_site = True


# Register your models here.
admin.site.register(Invite, InviteAdmin)
