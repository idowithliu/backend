# Generated by Django 4.1.4 on 2022-12-20 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0002_alter_registry_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='registryitem',
            name='claimer_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]