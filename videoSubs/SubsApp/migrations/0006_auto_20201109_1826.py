# Generated by Django 3.1.2 on 2020-11-09 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SubsApp', '0005_video_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='ytId',
            field=models.CharField(max_length=1000),
        ),
    ]
