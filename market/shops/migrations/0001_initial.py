# Generated by Django 4.2.1 on 2023-07-13 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=280, verbose_name='название баннера')),
                ('description', models.TextField(max_length=280, null=True, verbose_name='описание баннера')),
                ('image', models.ImageField(upload_to='media/banners/', verbose_name='изображение баннера')),
                ('active', models.BooleanField(default=True, verbose_name='статус активности баннера')),
            ],
            options={
                'verbose_name': 'баннер',
                'verbose_name_plural': 'баннеры',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('product_in_stock', models.BooleanField(default=True, verbose_name='товар в наличии')),
                ('free_shipping', models.BooleanField(default=False, verbose_name='бесплатная доставка')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offers', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('delivery', models.CharField(choices=[('ORDINARY', 'Обычная'), ('EXPRESS', 'Экспрес')], default='ORDINARY', max_length=8, verbose_name='доставка')),
                ('citi', models.CharField(max_length=100, verbose_name='город')),
                ('address', models.CharField(max_length=200, verbose_name='адрес')),
                ('pay', models.CharField(choices=[('ONLINE', 'Онлайн'), ('SOMEONE', 'Онлайн со случайного чужого счета')], default='ONLINE', max_length=8, verbose_name='доставка')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('custom_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_index', models.SmallIntegerField(unique=True, verbose_name='порядковый индекс')),
                ('name', models.CharField(max_length=100, verbose_name='статус заказа')),
            ],
            options={
                'verbose_name': 'статус заказа',
                'verbose_name_plural': 'статусы заказа',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='название')),
                ('phone_number', models.CharField(max_length=13, verbose_name='номер телефона')),
                ('email', models.EmailField(max_length=100, verbose_name='почта')),
                ('products', models.ManyToManyField(related_name='shops', through='shops.Offer', to='products.product', verbose_name='товары в магазине')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatusChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='время изменения')),
                ('dst_status_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders_order_change_dst', to='shops.orderstatus')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shops.order')),
                ('src_status_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders_order_change_src', to='shops.orderstatus')),
            ],
            options={
                'verbose_name': 'изменение статуса заказа',
                'verbose_name_plural': 'изменение статусов заказов',
            },
        ),
        migrations.CreateModel(
            name='OrderOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.SmallIntegerField(verbose_name='количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shops.offer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shops.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='offer',
            field=models.ManyToManyField(related_name='orders', through='shops.OrderOffer', to='shops.offer', verbose_name='предложение'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='shops.orderstatus', verbose_name='статус'),
        ),
        migrations.AddField(
            model_name='offer',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shops.shop'),
        ),
    ]
