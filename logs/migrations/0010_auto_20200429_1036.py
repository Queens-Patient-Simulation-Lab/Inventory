# Generated by Django 3.0.3 on 2020-04-29 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0009_auto_20200428_2105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': ['-time']},
        ),
    ]