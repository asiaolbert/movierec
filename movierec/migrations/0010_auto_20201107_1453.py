# Generated by Django 3.1.3 on 2020-11-07 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movierec', '0009_auto_20201107_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='timestamp',
            field=models.IntegerField(),
        ),
    ]
