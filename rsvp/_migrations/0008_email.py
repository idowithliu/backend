# Generated by Django 4.1.4 on 2023-03-03 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0007_alter_invite_pseudo_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('invite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='rsvp.invite')),
            ],
        ),
    ]