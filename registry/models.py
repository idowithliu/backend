from django.db import models

# Create your models here.
class RegistryItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name