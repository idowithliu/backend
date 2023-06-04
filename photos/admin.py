from django.contrib import admin
from .models import Photo

# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    exclude = ('id',)

admin.site.register(Photo, PhotoAdmin)