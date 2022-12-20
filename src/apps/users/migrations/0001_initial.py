# Generated by Django 3.2.9 on 2021-11-06 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, help_text='HT__FIRST_NAME', max_length=50, verbose_name='VN__FIRST_NAME')),
                ('last_name', models.CharField(blank=True, help_text='HT__LAST_NAME', max_length=50, verbose_name='VN__LAST_NAME')),
                ('email', models.EmailField(db_index=True, help_text='HT__EMAIL', max_length=254, unique=True, verbose_name='VN__EMAIL')),
                ('is_staff', models.BooleanField(default=True, help_text='HT__IS_STAFF', verbose_name='VN__IS_STAFF')),
                ('is_active', models.BooleanField(default=True, help_text='HT__IS_ACTIVE', verbose_name='VN__IS_ACTIVE')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'VN__USER',
                'verbose_name_plural': 'VN__USERS',
                'ordering': ('email',),
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'VN__TOKEN',
                'verbose_name_plural': 'VN__TOKENS',
            },
        ),
    ]