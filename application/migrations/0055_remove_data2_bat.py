# Generated by Django 4.0.6 on 2024-07-25 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0054_rename_pr_data2_bat_rename_dateray_ray2_dateray_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data2',
            name='Bat',
        ),
    ]
