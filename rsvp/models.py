from django.db import models
import uuid
# from registry.models import Fund

# Create your models here.


def next_id():
    try:
        return Invite.objects.latest('pseudo_id').pseudo_id + 1
    except:
        return 1


class Invite(models.Model):
    family_name = models.CharField(max_length=200)
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
    pseudo_id = models.IntegerField(
        unique=True, default=next_id)
    invite_url = models.URLField(verbose_name="Unique RSVP Link")
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

    @property
    def number_of_guests(self) -> int:
        return Guest.objects.filter(invite__uuid=self.uuid).__len__()


class Email(models.Model):
    address = models.EmailField(verbose_name="Email Address")
    invite = models.ForeignKey(
        Invite, related_name="emails", on_delete=models.CASCADE)

    def __str__(self):
        return self.address


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

    def get_absolute_url(self):
        return f"/rsvp?userID={self.invite.uuid}"


class Info(models.Model):
    @property
    def total_rsvp_yes(self) -> int:
        return Guest.objects.filter(is_attending=True).__len__()

    total_rsvp_yes.fget.short_description = "Total guests who RSVP'd \"Yes\""

    @property
    def total_rsvp(self) -> int:
        return Guest.objects.filter(invite__finished=True).__len__()

    total_rsvp.fget.short_description = "Total guests who completed RSVP"

    @property
    def total_invited(self) -> int:
        return Guest.objects.all().__len__()

    total_invited.fget.short_description = "Total guests who were invited"

    class Meta:
        verbose_name_plural = "Guest Summary"
