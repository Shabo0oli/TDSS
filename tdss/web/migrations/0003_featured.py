# Generated by Django 2.2.4 on 2019-08-23 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20190823_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='Featured',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Reliability', models.IntegerField(default=0)),
                ('Popularity', models.IntegerField(default=0)),
                ('Polarity', models.IntegerField(default=0)),
                ('Tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Tweet')),
            ],
        ),
    ]
