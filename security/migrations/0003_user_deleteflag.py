# Generated by Django 2.2.7 on 2020-02-03 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0002_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='deleteFlag',
            field=models.BooleanField(default=False),
        ),
    ]
