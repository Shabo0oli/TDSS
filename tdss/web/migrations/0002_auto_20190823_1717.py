# Generated by Django 2.2.4 on 2019-08-23 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='Location',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='tweet',
            name='Source',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tweet',
            name='Username',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]