# Generated by Django 4.2.1 on 2023-08-02 17:05

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("catalog", "0001_initial"),
        ("products", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShopItemDiscount",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, verbose_name="название скидки")),
                ("description", models.TextField(max_length=150, verbose_name="Описание скидки")),
                (
                    "discount_amount",
                    models.DecimalField(decimal_places=2, max_digits=10, verbose_name="размер скидки"),
                ),
                ("discount_amount_type", models.PositiveSmallIntegerField(choices=[(1, "проценты"), (2, "сумма")])),
                ("active", models.BooleanField(verbose_name="скидка активна")),
                ("start_date", models.DateTimeField(verbose_name="дата начала действия скидки")),
                ("end_date", models.DateTimeField(verbose_name="дата окончания действия скидки")),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True, related_name="%(class)s", to="catalog.catalog", verbose_name="категории товаров"
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        blank=True, related_name="%(class)s", to="products.product", verbose_name="товары"
                    ),
                ),
            ],
            options={
                "verbose_name": "скидка на товар в магазине",
                "verbose_name_plural": "скидки на товары в магазине",
            },
        ),
        migrations.CreateModel(
            name="CartItemDiscount",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, verbose_name="название скидки")),
                ("description", models.TextField(max_length=150, verbose_name="Описание скидки")),
                (
                    "discount_amount",
                    models.DecimalField(decimal_places=2, max_digits=10, verbose_name="размер скидки"),
                ),
                ("discount_amount_type", models.PositiveSmallIntegerField(choices=[(1, "проценты"), (2, "сумма")])),
                ("active", models.BooleanField(verbose_name="скидка активна")),
                ("start_date", models.DateTimeField(verbose_name="дата начала действия скидки")),
                ("end_date", models.DateTimeField(verbose_name="дата окончания действия скидки")),
                (
                    "total_price_of_cart",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Скидка может быть установлена на стоимость товаров в корзине.",
                        max_digits=10,
                        null=True,
                        verbose_name="Минимальная цена товаров в корзине",
                    ),
                ),
                (
                    "amount_product_in_cart",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Скидка может быть установлена на количество товаров в корзине.",
                        null=True,
                        verbose_name="Минимальное количество товаров в корзине",
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True, related_name="%(class)s", to="catalog.catalog", verbose_name="категории товаров"
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        blank=True, related_name="%(class)s", to="products.product", verbose_name="товары"
                    ),
                ),
            ],
            options={
                "verbose_name": "скидка на товар в корзине",
                "verbose_name_plural": "скидки на товары в корзине",
            },
        ),
    ]
