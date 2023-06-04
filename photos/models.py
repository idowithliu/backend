from django.db import models

# Create your models here.
class Photo(models.Model):
    id = models.IntegerField(verbose_name="Photo ID", primary_key=True)
    image = models.ImageField(verbose_name="Image Data")
