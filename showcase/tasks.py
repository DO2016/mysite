import random

from django_rq import job

from showcase.models import Product, Ingredient, CustomUser, Order, OrderItem


def get_rnd(arg_list):
    return random.choice(arg_list)

@job
def create_rnd_sales(*args, **kwargs):
    all_products = list(Product.objects.all())
    all_customers = list(CustomUser.objects.all())
    order_list = [Order(customer=get_rnd(all_customers), created_date = '2016-09-02', updated_date = '2016-09-02') for x in xrange(100)]
    Order.objects.bulk_create(order_list)
    all_orders = list(Order.objects.all())
    order_items_list = [OrderItem(product=get_rnd(all_products), order=get_rnd(all_orders)) for x in xrange(1000)]
    OrderItem.objects.bulk_create(order_items_list)
    return order_items_list