# Generated by Django 5.0.6 on 2024-06-14 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sourcemodel',
            name='status',
        ),
    ]
