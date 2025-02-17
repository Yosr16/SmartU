# Generated by Django 5.0.3 on 2024-04-20 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_followerscount_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('culturel', 'Culturel'), ('scientifique', 'Scientifique')], max_length=20)),
                ('titre', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='EventClub',
            fields=[
                ('evenement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.evenement')),
                ('club', models.CharField(max_length=100)),
            ],
            bases=('core.evenement',),
        ),
        migrations.CreateModel(
            name='EventSocial',
            fields=[
                ('evenement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.evenement')),
                ('prix', models.FloatField()),
            ],
            bases=('core.evenement',),
        ),
        migrations.CreateModel(
            name='Logement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=200)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'ouvrier'), (2, 'technicien'), (3, 'PFE')])),
                ('sujet', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=200)),
                ('moyen_transport', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
        ),
    ]
