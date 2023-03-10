# Generated by Django 4.1.4 on 2023-02-25 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0004_remove_invite_funds_delete_fund'),
        ('registry', '0008_delete_fundcontrib'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FundContrib',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Contribution Amount')),
                ('contributer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fund_contribs', to='rsvp.invite')),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='registry.fund')),
            ],
            options={
                'verbose_name': 'Honeymoon Fund Contribution',
            },
        ),
    ]
