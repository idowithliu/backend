from django.contrib import admin
from .models import Invite, Guest
from registry.models import FundContrib
# from registry.models import Fund


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('name', 'dietary_restrictions', 'is_attending',)


class FundContribInline(admin.TabularInline):
    model = FundContrib
    fields = ('amount', 'fund',)


# class FundsInline(admin.TabularInline):
#     model = Fund
#     fields = ('amount',)


class InviteAdmin(admin.ModelAdmin):
    inlines = [GuestInline, FundContribInline]
    list_display = ("family_name", "finished", "invite_url", "email",)
    exclude = ("invite_url", "finished", 'pseudo_id',)
    view_on_site = True


# Register your models here.
admin.site.register(Invite, InviteAdmin)
