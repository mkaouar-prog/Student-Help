# Generated by Django 5.0.3 on 2024-05-19 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_event_contactinfo_event_titre_alter_event_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('location', models.TextField()),
                ('description', models.TextField()),
                ('contactinfo', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Logement', to='core.category')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='logement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.logement'),
        ),
    ]
