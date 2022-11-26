# Generated by Django 4.1.3 on 2022-11-26 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0006_remove_swaggerimport_status_swaggerimport_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="swaggerimport",
            name="project",
            field=models.ForeignKey(
                help_text="HT__PROJECT",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="swagger_imports",
                to="projects.project",
                verbose_name="VN__PROJECT",
            ),
        ),
    ]
