# Generated by Django 4.1.4 on 2022-12-31 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registryitem',
            name='url',
            field=models.URLField(default='https://example.com/item', verbose_name='Link to Purchase Site'),
            preserve_default=False,
        ),
    ]
