# Generated by Django 4.1.3 on 2022-11-29 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0009_alter_swaggerimport_log_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="swaggerimport",
            name="log",
            field=models.TextField(
                blank=True,
                default="",
                help_text="HT__LOG",
                verbose_name="VN__LOG",
            ),
        ),
        migrations.AlterField(
            model_name="swaggerimport",
            name="swagger_content",
            field=models.TextField(
                blank=True,
                default="",
                help_text="HT__SWAGGER_CONTENT",
                verbose_name="VN__SWAGGER_CONTENT",
            ),
        ),
        migrations.AlterField(
            model_name="swaggerimport",
            name="swagger_url",
            field=models.TextField(
                blank=True,
                default="",
                help_text="HT__SWAGGER_URL",
                verbose_name="VN__SWAGGER_URL",
            ),
        ),
    ]
