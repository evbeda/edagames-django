# Generated by Django 2.2.20 on 2021-06-08 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0014_auto_20210608_1404'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='players',
            new_name='match_members',
        ),
    ]
