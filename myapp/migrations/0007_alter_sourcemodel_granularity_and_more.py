# Generated by Django 5.0.6 on 2024-06-21 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_sourcemodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcemodel',
            name='granularity',
            field=models.CharField(default='National', max_length=255),
        ),
        migrations.AlterField(
            model_name='sourcemodel',
            name='panel_group',
            field=models.CharField(blank=True, default='DKM', max_length=255),
        ),
    ]
