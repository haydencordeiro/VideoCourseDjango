# Generated by Django 3.1.2 on 2020-11-09 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SubsApp', '0002_auto_20201108_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canAccess', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='canAccess', to='SubsApp.subtype')),
                ('subType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subType', to='SubsApp.subtype')),
            ],
        ),
    ]