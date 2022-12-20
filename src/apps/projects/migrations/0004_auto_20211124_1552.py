# Generated by Django 3.2.9 on 2021-11-24 12:52

import apps.media.models.fields.file
import apps.projects.models.project_asset
from django.db import migrations, models
import django.db.models.deletion
import jnt_django_toolbox.models.fields.enum


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_file'),
        ('projects', '0003_remove_project_is_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='FigmaIntegration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, default='', help_text='HT__TOKEN', max_length=128, verbose_name='VN__TOKEN')),
            ],
            options={
                'verbose_name': 'VN__FIGMA_INTEGRATION',
                'verbose_name_plural': 'VN__FIGMA_INTERGRATIONS',
            },
        ),
        migrations.CreateModel(
            name='ProjectAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='HT__CREATED_AT', verbose_name='VN__CREATED_AT')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='HT__UPDATED_AT', verbose_name='VN__UPDATED_AT')),
                ('source', jnt_django_toolbox.models.fields.enum.EnumField(choices=[('FIGMA', 'CH__FIGMA')], default='FIGMA', enum=apps.projects.models.project_asset.ProjectAssetSource, help_text='HT__PROJECT_ASSET_SOURCE', verbose_name='VN__PROJECT_ASSET_SOURCE')),
                ('file', apps.media.models.fields.file.FileField(blank=True, help_text='HT__FILE', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='media.file', verbose_name='VN__FILE')),
            ],
            options={
                'verbose_name': 'VN__PROJECT_ASSET',
                'verbose_name_plural': 'VN__PROJECTS_ASSETS',
                'ordering': ('-created_at',),
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='members',
        ),
        migrations.DeleteModel(
            name='ProjectMember',
        ),
        migrations.AddField(
            model_name='projectasset',
            name='project',
            field=models.ForeignKey(help_text='HT__PROJECT', null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='VN__PROJECT'),
        ),
        migrations.AddField(
            model_name='figmaintegration',
            name='project',
            field=models.OneToOneField(help_text='HT__PROJECT', on_delete=django.db.models.deletion.CASCADE, related_name='figma_integration', to='projects.project', verbose_name='VN__PROJECT'),
        ),
    ]