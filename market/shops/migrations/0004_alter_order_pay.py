# Generated by Django 4.2.1 on 2023-07-26 05:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shops", "0003_rename_citi_order_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="pay",
            field=models.CharField(
                choices=[("ONLINE", "Онлайн"), ("SOMEONE", "Онлайн со случайного чужого счета")],
                default="ONLINE",
                max_length=8,
                verbose_name="вид оплаты",
            ),
        ),
    ]
