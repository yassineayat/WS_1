# Generated by Django 4.0.6 on 2024-07-23 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0048_cwsi_cw'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cwsi',
            name='cw',
        ),
    ]
