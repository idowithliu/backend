from django.db import models
from rsvp.models import Guest, Invite
from django.core.exceptions import ValidationError

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
    photo_url = models.URLField(verbose_name="Photo URL")

    price = models.IntegerField(blank=True, null=True)

    claimer = models.ForeignKey(
        Invite, related_name="claimed_items", on_delete=models.CASCADE, null=True, blank=True)

    registry = models.ForeignKey(
        Registry, related_name="registry_items", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Fund(models.Model):
    name = models.CharField(max_length=200)
    goal = models.IntegerField()
    background_photo = models.URLField(verbose_name="Link to Background Photo")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/registry"

    @property
    def total_amount_raised(self) -> int:
        total_raised = 0
        contributions = FundContrib.objects.filter(fund__id=self.id)
        for contribution in contributions:
            total_raised += contribution.amount
        return total_raised


class FundContrib(models.Model):
    contributer = models.ForeignKey(
        Invite, on_delete=models.CASCADE, related_name="fund_contribs")
    fund = models.ForeignKey(
        Fund, on_delete=models.CASCADE, related_name="contributions")
    amount = models.IntegerField(verbose_name="Contribution Amount")
    is_cleaned = False

    def __str__(self):
        return f"from {self.contributer.family_name} to {self.fund.name}"

    def clean(self):
        self.is_cleaned = True
        if self.amount <= 0:
            raise ValidationError("Contribution amount must be positive")
        super(FundContrib, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(FundContrib, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Fund Contribution"
        verbose_name_plural = "Fund Contributions"
