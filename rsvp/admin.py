from django.contrib import admin
from .models import Invite, Guest, Email, Info
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
    list_display = ("family_name", "finished",
                    "number_of_guests", "invite_url",)
    exclude = ("invite_url", "finished", 'pseudo_id',)
    view_on_site = True


class GuestAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ("name", "is_attending",)
    view_on_site = True


class InfoAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ('total_rsvp_yes', 'total_rsvp', 'total_invited',)


# Register your models here.
admin.site.register(Invite, InviteAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(Guest, GuestAdmin)
