from django.db import models
from rsvp.models import Guest

# Create your models here.


class Registry(models.Model):
    name = models.CharField(
        max_length=200, help_text="Ex. \"Kitchen\", or \"Appliances\"")
    visible = models.BooleanField(
        verbose_name="Visible on Site (Published)", default=False)

    def __str__(self):
        return f"{self.name} ({'PUBLISHED' if self.visible else 'UNPUBLISHED'})"

    class Meta:
        verbose_name_plural = "Registries"

    def get_absolute_url(self):
        return f"/registry"


class RegistryItem(models.Model):
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True, unique=True)
    url = models.URLField(verbose_name="Link to Purchasing Site")

    price = models.IntegerField(blank=True, null=True)

    claimer = models.ForeignKey(
        Guest, related_name="claimed_items", on_delete=models.CASCADE, null=True, blank=True)

    registry = models.ForeignKey(
        Registry, related_name="registry_items", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
