# Generated by Django 3.0.3 on 2020-02-28 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='users',
            new_name='user',
        ),
    ]
