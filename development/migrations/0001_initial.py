# Generated by Django 2.2.20 on 2021-04-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_one', models.CharField(max_length=30)),
                ('player_two', models.CharField(max_length=30)),
                ('score_p_one', models.IntegerField()),
                ('score_p_two', models.IntegerField()),
            ],
        ),
    ]
