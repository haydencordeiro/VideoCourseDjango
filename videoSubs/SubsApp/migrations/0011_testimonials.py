# Generated by Django 3.1.2 on 2020-11-10 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SubsApp', '0010_subscription_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=1000)),
            ],
        ),
    ]
