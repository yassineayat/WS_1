# Generated by Django 3.2.14 on 2023-05-14 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0033_alter_data_d'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='et0',
            name='dt',
        ),
        migrations.AddField(
            model_name='et0',
            name='i',
            field=models.IntegerField(null=True),
        ),
    ]
