# Generated by Django 2.2.4 on 2020-11-24 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0164_mediafile'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='filename',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
    ]