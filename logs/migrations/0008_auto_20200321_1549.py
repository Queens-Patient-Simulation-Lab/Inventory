# Generated by Django 2.2.7 on 2020-03-21 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0007_auto_20200304_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteminfologs',
            name='kghID',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='iteminfologs',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True),
        ),
    ]