# Generated by Django 5.0.6 on 2024-06-21 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_sourcemodel_current_status_sourcemodel_next_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sourcemodel',
            name='current_status',
        ),
    ]
