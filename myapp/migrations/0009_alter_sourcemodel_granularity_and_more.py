# Generated by Django 5.0.6 on 2024-06-21 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_sourcemodel_granularity'),
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
            field=models.CharField(default='DKM', max_length=255),
        ),
    ]
