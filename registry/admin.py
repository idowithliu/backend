from django.contrib import admin
from .models import Registry, RegistryItem


class RegistryItemInline(admin.TabularInline):
    model = RegistryItem
    fields = ('name', 'claimer', 'id')


class RegistryAdmin(admin.ModelAdmin):
    inlines = [RegistryItemInline]
    list_display = ('name', 'visible',)
    view_on_site = True


# Register your models here.
admin.site.register(Registry, RegistryAdmin)
