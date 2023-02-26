from django.db import models
import uuid
# from registry.models import Fund

# Create your models here.


def next_id():
    return Invite.objects.latest('pseudo_id').pseudo_id + 1


class Invite(models.Model):
    family_name = models.CharField(max_length=200)
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
    pseudo_id = models.IntegerField(
        unique=True, default=next_id)
    invite_url = models.URLField(verbose_name="Unique RSVP Link")
    email = models.EmailField(verbose_name="Email Address")
    finished = models.BooleanField(
        verbose_name="Has Completed RSVP", default=False)

    def __str__(self):
        return self.family_name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
            self.invite_url = f"https://idowithliu.com/rsvp?userID={self.uuid}"
        super(Invite, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/rsvp?userID={self.uuid}"


class Guest(models.Model):
    invite = models.ForeignKey(
        Invite, related_name="guests", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    dietary_restrictions = models.CharField(
        null=True, blank=True, max_length=200)
    is_attending = models.BooleanField(
        verbose_name="Is Attending", null=True, blank=True)

    def __str__(self):
        return self.name
