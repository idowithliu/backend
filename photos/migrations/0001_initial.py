# Generated by Django 4.1.4 on 2023-06-04 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Photo ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image Data')),
            ],
        ),
    ]
