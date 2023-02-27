# Generated by Django 4.1.4 on 2023-02-26 01:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0004_remove_invite_funds_delete_fund'),
        ('registry', '0011_fund_goal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registryitem',
            name='claimer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='claimed_items', to='rsvp.invite'),
        ),
    ]