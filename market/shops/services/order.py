from decimal import Decimal
from typing import Any
from django.db.models import F, Sum
from django.db import transaction
from django.conf import settings

from cart.models import CartItem, Cart
from shops.models import OrderOffer, OrderStatusChange, OrderStatus, Order
MIN_PRICE_OFFER = Decimal(2000.00)
DELIVERY_EXPRESS = Decimal(500.00)
DELIVERY_ORDINARY = Decimal(200.00)

def pryce_delivery(r_user: Any) -> dict:
    """Расчет стоимости доставки"""
    cart_list = (
        CartItem.objects.filter(cart__user=r_user)
        .select_related("offer__product", "offer__shop")
        .annotate(summ_offer=F("offer__price") * F("quantity"))
    )

    cart_count_shop = cart_list.all().values_list("offer__shop").distinct().count()
    total_cost = Decimal(cart_list.all().aggregate(summ=Sum("summ_offer"))["summ"])

    if total_cost > MIN_PRICE_OFFER and cart_count_shop == 1:
        total_cost_delivery_ordinary = total_cost
    else:
        total_cost_delivery_ordinary = total_cost + DELIVERY_ORDINARY
    total_cost_delivery_express = total_cost + DELIVERY_EXPRESS
    return {
        "total_cost_ordinary": total_cost_delivery_ordinary,
        "total_cost_express": total_cost_delivery_express,
        "delivery_express": DELIVERY_EXPRESS,
        "delivery_ordinary": DELIVERY_ORDINARY,
        "query_set_cart": cart_list,
    }


@transaction.atomic
def save_order_model(r_user: Any, r_post: Any, r_session: Any) -> int:
    """
    Сохранение заказа и истории изменения статуса
    Стирание корзины
    """
    cart_dict = pryce_delivery(r_user)

    if r_post.get("delivery") == "ORDINARY":
        total_cost = cart_dict["total_cost_ordinary"]
    else:
        total_cost = cart_dict["total_cost_express"]

    new_order = Order()
    new_order.custom_user = r_user
    new_order.status = OrderStatus.objects.get(sort_index=1)
    new_order.delivery = r_post["delivery"]
    new_order.city = r_post["city"]
    new_order.address = r_post["address"]
    new_order.pay = r_post["pay"]
    new_order.total_cost = total_cost
    new_order.save()

    for item_cart_i in cart_dict["query_set_cart"]:
        cart2order = OrderOffer()
        cart2order.offer = item_cart_i.offer
        cart2order.order = new_order
        cart2order.count = item_cart_i.quantity
        cart2order.price = item_cart_i.summ_offer
        cart2order.save()

    order_status = OrderStatusChange()
    order_status.order = new_order
    order_status.src_status = OrderStatus.objects.get(sort_index=1)
    order_status.dst_status = OrderStatus.objects.get(sort_index=5)
    order_status.save()
    Cart.objects.get(user=r_user).delete()
    r_session[settings.CART_SESSION_ID] = {}
    return new_order.pk
