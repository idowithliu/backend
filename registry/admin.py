from django.contrib import admin
from .models import Registry, RegistryItem, Fund, FundContrib


class RegistryItemInline(admin.TabularInline):
    model = RegistryItem
    fields = ('name', 'url', 'claimer', 'id')


class RegistryAdmin(admin.ModelAdmin):
    inlines = [RegistryItemInline]
    list_display = ('name', 'visible',)
    view_on_site = True


class FundAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ('name', 'total_amount_raised',)

    def total_amount_raised(self, obj: Fund):
        return f"${obj.total_amount_raised}"


# Register your models here.
admin.site.register(Registry, RegistryAdmin)
admin.site.register(Fund, FundAdmin)
