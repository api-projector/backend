# Generated by Django 3.2.9 on 2021-11-07 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='is_public',
        ),
    ]
