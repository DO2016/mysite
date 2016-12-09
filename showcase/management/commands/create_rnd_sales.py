from django.core.management.base import BaseCommand, CommandError
from showcase.models import Product, Ingredient, CustomUser, Order, OrderItem
import random

class Command(BaseCommand):
    @staticmethod
    def _get_rnd(arg_list):
        return random.choice(arg_list)

    def handle(self, *args, **options):
        all_products = list(Product.objects.all())
        all_customers = list(CustomUser.objects.all())

        order_list = [Order(customer=self._get_rnd(all_customers), created_date = '2016-09-02', updated_date = '2016-09-02') for x in xrange(100)]
        Order.objects.bulk_create(order_list)
        all_orders = list(Order.objects.all())

        order_items_list = [OrderItem(product=self._get_rnd(all_products), order=self._get_rnd(all_orders)) for x in xrange(1000)]
        OrderItem.objects.bulk_create(order_items_list)
        
