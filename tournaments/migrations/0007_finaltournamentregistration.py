# Generated by Django 2.2.20 on 2022-10-19 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0006_tournament_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalTournamentRegistration',
            fields=[
                ('tournamentregistration_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tournaments.TournamentRegistration')),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='championship', to='tournaments.Championship')),
            ],
            bases=('tournaments.tournamentregistration',),
        ),
    ]
