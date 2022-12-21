# Generated by Django 4.1.4 on 2022-12-18 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Ex. "Kitchen", or "Appliances"', max_length=200)),
                ('visible', models.BooleanField(default=False, verbose_name='Visible on Site (Published)')),
            ],
        ),
        migrations.CreateModel(
            name='RegistryItem',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Featured image')),
                ('claimer', models.CharField(blank=True, max_length=200, null=True)),
                ('registry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registry_items', to='registry.registry')),
            ],
        ),
    ]
