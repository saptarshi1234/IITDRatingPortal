# Generated by Django 3.0.4 on 2020-03-23 16:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200322_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ban_days',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='banned_on',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
