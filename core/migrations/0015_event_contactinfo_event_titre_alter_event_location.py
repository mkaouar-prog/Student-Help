# Generated by Django 5.0.3 on 2024-05-19 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_carpooling_contactinfo_carpooling_depart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='contactinfo',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='titre',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
