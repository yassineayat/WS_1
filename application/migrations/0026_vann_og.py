# Generated by Django 3.2.14 on 2022-10-19 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0025_rename_vanne_vann'),
    ]

    operations = [
        migrations.AddField(
            model_name='vann',
            name='og',
            field=models.FloatField(null=True),
        ),
    ]
