# Generated by Django 3.1.2 on 2020-11-09 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SubsApp', '0003_typeaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtype',
            name='discountPrice',
            field=models.IntegerField(default=0),
        ),
    ]
