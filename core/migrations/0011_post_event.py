# Generated by Django 5.0.3 on 2024-04-29 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_category_carpooling_absence_post_categories_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='event',
            field=models.ManyToManyField(to='core.event'),
        ),
    ]
