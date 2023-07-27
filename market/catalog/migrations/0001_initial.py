# Generated by Django 4.2.1 on 2023-07-18 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Catalog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(help_text="наименование", max_length=100)),
                (
                    "image",
                    models.FileField(upload_to="catalog/icon/", verbose_name="картинка"),
                ),
                (
                    "is_featured",
                    models.BooleanField(default=False, verbose_name="избранная категория"),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="catalog.catalog",
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
                "ordering": ["name"],
            },
        ),
    ]
