# Generated by Django 4.0.2 on 2022-08-14 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_messageus'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageus',
            name='is_client',
            field=models.BooleanField(default=False),
        ),
    ]
