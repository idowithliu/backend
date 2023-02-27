# Generated by Django 4.1.4 on 2023-02-25 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0002_invite_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('amount', models.IntegerField(verbose_name='Total Amount Raised')),
            ],
        ),
        migrations.AddField(
            model_name='invite',
            name='funds',
            field=models.ManyToManyField(to='rsvp.fund'),
        ),
    ]