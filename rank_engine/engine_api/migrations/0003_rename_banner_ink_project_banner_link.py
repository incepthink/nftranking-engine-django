# Generated by Django 3.2.12 on 2022-03-11 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine_api', '0002_auto_20220310_1956'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='banner_ink',
            new_name='banner_link',
        ),
    ]