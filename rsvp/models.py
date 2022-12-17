from django.db import models
import uuid

# Create your models here.
class Invite(models.Model):
    family_name = models.CharField(max_length=200)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    def __str__(self):
        return self.family_name

class Guest(models.Model):
    invite = models.ForeignKey(Invite, related_name="guests", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dietary_restrictions = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.name