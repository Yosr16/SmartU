# Generated by Django 5.0.3 on 2024-04-27 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_transport_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transport',
            name='moyen_transport',
            field=models.CharField(choices=[('Avion', 'Avion'), ('Train', 'Train'), ('Voiture', 'Voiture'), ('Bus', 'Bus')], max_length=50),
        ),
    ]