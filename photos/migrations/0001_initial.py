# Generated by Django 4.1.4 on 2023-06-26 20:42

from django.db import migrations, models
import photos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=photos.models._func, verbose_name='Image Data')),
            ],
        ),
    ]
