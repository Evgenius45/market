# Generated by Django 4.2.1 on 2023-08-01 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models
import taggit.managers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("taggit", "0005_auto_20220424_2025"),
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Import",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source", models.CharField(max_length=255, verbose_name="имя файла или URL для импорта")),
                ("start_time", models.DateTimeField(null=True, verbose_name="дата и время начала импорта")),
                ("end_time", models.DateTimeField(null=True, verbose_name="дата и время окончания импорта")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "В ожидании"),
                            ("running", "В процессе выполнения"),
                            ("completed", "Выполнен"),
                            ("failed", "Завершен с ошибкой"),
                        ],
                        default="pending",
                        max_length=10,
                        verbose_name="статус импорта",
                    ),
                ),
                ("imported_count", models.IntegerField(default=0, verbose_name="количество импортированных товаров")),
                ("errors", models.JSONField(default=list, verbose_name="список ошибок при импорте")),
                ("email", models.EmailField(max_length=254, null=True, verbose_name="email получателя уведомления")),
                (
                    "task_id",
                    models.CharField(blank=True, max_length=36, null=True, verbose_name="идентификатор задачи"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(db_index=True, max_length=512, verbose_name="наименование")),
                ("limited_edition", models.BooleanField(default=False, verbose_name="ограниченный тираж")),
                ("index", models.PositiveIntegerField(default=0, verbose_name="индекс сортировки")),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.product_preview_directory_path,
                        verbose_name="предварительный просмотр",
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="описание")),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="category",
                        to="catalog.catalog",
                        verbose_name="категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "продукт",
                "verbose_name_plural": "продукты",
            },
        ),
        migrations.CreateModel(
            name="Property",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=512, verbose_name="наименование")),
            ],
            options={
                "verbose_name": "свойство",
                "verbose_name_plural": "свойства",
            },
        ),
        migrations.CreateModel(
            name="ProductProperty",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(max_length=128, verbose_name="значение")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="products.product")),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="products.property", verbose_name="свойство"
                    ),
                ),
            ],
            options={
                "verbose_name": "свойство продукта",
                "verbose_name_plural": "свойства продуктов",
                "unique_together": {("product", "property")},
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "image",
                    models.ImageField(
                        upload_to=products.models.product_images_directory_path, verbose_name="изображение"
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="описание")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_images",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "изображения продуктов",
                "verbose_name_plural": "изображение продукта",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="property",
            field=models.ManyToManyField(
                through="products.ProductProperty", to="products.property", verbose_name="характеристики"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="tags",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.CreateModel(
            name="Browsing_history",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("data_at", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="products", to="products.product"
                    ),
                ),
                ("users", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "просмотр продута",
                "verbose_name_plural": "просмотр продуктов",
                "ordering": ["-data_at"],
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")], verbose_name="оценка"
                    ),
                ),
                ("review_text", models.TextField(max_length=500, null=True, verbose_name="текст отзыва")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="products.product", verbose_name="продукт"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="покупатель",
                    ),
                ),
            ],
            options={
                "verbose_name": "отзыв",
                "verbose_name_plural": "отзывы",
                "unique_together": {("user", "product")},
            },
        ),
    ]
