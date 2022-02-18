# Generated by Django 3.2.9 on 2021-11-06 14:02

import apps.projects.models.project
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='HT__CREATED_AT', verbose_name='VN__CREATED_AT')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='HT__UPDATED_AT', verbose_name='VN__UPDATED_AT')),
                ('id', models.CharField(default=apps.projects.models.project.get_new_id, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('is_public', models.BooleanField(default=False, help_text='HT__IS_PUBLIC', verbose_name='VN__IS_PUBLIC')),
                ('title', models.CharField(help_text='HT__TITLE', max_length=255, verbose_name='VN__TITLE')),
                ('description', models.TextField(help_text='HT__DESCRIPTION', verbose_name='VN__DESCRIPTION')),
                ('db_name', models.CharField(blank=True, help_text='HT__DB_NAME', max_length=50, verbose_name='VN__DB_NAME')),
            ],
            options={
                'verbose_name': 'VN__PROJECT',
                'verbose_name_plural': 'VN__PROJECTS',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='HT__CREATED_AT', verbose_name='VN__CREATED_AT')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='HT__UPDATED_AT', verbose_name='VN__UPDATED_AT')),
                ('project', models.ForeignKey(help_text='HT__PROJECT', on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='VN__PROJECT')),
            ],
            options={
                'verbose_name': 'VN__PROJECT_MEMBER',
                'verbose_name_plural': 'VN__PROJECT_MEMBERS',
            },
        ),
    ]
