# Generated by Django 2.2.20 on 2021-06-08 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_auto_20210512_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]