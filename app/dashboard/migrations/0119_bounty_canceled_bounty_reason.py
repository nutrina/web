# Generated by Django 2.1.2 on 2018-11-27 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0118_merge_20181127_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='bounty',
            name='canceled_bounty_reason',
            field=models.TextField(blank=True, default='', verbose_name='Cancelation reason'),
        ),
    ]
