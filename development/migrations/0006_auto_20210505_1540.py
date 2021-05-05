# Generated by Django 2.2.20 on 2021-05-05 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0005_auto_20210505_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='bot_one',
            field=models.CharField(max_length=30, verbose_name='Player 1'),
        ),
        migrations.AlterField(
            model_name='match',
            name='bot_two',
            field=models.CharField(max_length=30, verbose_name='Player 2'),
        ),
        migrations.AlterField(
            model_name='match',
            name='date_match',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='match',
            name='score_p_one',
            field=models.IntegerField(verbose_name='Score 1'),
        ),
        migrations.AlterField(
            model_name='match',
            name='score_p_two',
            field=models.IntegerField(verbose_name='Score 2'),
        ),
    ]