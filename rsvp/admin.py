from django.contrib import admin
from .models import Invite, Guest

class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('name', 'dietary_restrictions')

class InviteAdmin(admin.ModelAdmin):
    inlines = [GuestInline]

# Register your models here.
admin.site.register(Invite, InviteAdmin)