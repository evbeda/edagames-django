# Generated by Django 2.2.20 on 2021-04-21 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('development', '0002_match_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='player_one',
            new_name='bot_one',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='player_two',
            new_name='bot_two',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='date',
            new_name='date_match',
        ),
        migrations.AddField(
            model_name='match',
            name='board_id',
            field=models.IntegerField(default=12345),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='user_one',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_one', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='user_two',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='user_two', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
