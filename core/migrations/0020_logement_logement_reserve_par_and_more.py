# Generated by Django 5.0.3 on 2024-04-28 18:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_remove_transport_est_reserve'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='logement',
            name='logement_reserve_par',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='logement',
            name='nbr_logements_reserves',
            field=models.IntegerField(default=0),
        ),
    ]
