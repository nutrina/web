# Generated by Django 2.2.4 on 2020-06-26 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0123_auto_20200617_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sybil_score',
            field=models.IntegerField(default=-1),
        ),
    ]
