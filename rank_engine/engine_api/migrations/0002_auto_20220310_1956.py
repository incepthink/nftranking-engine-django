# Generated by Django 3.2.12 on 2022-03-10 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='banner_ink',
            field=models.CharField(default='none', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='total_supply',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='volume',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
