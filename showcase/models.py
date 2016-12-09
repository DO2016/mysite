from __future__ import unicode_literals

from datetime import datetime
from tastypie.models import create_api_key
from tastypie.models import ApiKey

from django.db import models
from django.db import connection
from django.dispatch import receiver
from django.utils import six, timezone
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.contrib.auth.models import User, AbstractUser, UserManager, AbstractBaseUser, PermissionsMixin
from django.dispatch.dispatcher import Signal


# Create your models here.
models.signals.post_save.connect(create_api_key, sender=User)


class ProductManager(models.Manager):
    def all_published(self):
        return self.select_related().filter(is_published=True).annotate(sum_ings_price = Sum('ings__price'))


class OrderManager(models.Manager):
    def _validate(self, date_text):
        try:
            return date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d')
        except ValueError:
            return False

    def my_custom_sql(self, start_date, end_date, step='day'):
        with connection.cursor() as cursor:
            query = "select * from showcase_fun_get_stat('{0}', '{1}', '{2}')".format(str(start_date), str(end_date), step)
            cursor.execute(query)
            res =  cursor.fetchall()
            return res

    def get_report_data(self, start_date, end_date, step='day'):
        allowed_steps = ['day', 'week', 'month']

        if step not in allowed_steps:
            step = 'day'

        if self._validate(start_date) and self._validate(end_date):
            result = self.my_custom_sql(start_date, end_date, step)
            return result
        return []


class AbstractModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Product created date')
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Product last update date')
    
    class Meta:
        abstract = True       


class Currency(AbstractModel):
    # https://www.fxclub.org/kody-valyut-mira/
    name = models.CharField(max_length=200, verbose_name='currency name', unique=True)
    char_code = models.CharField(max_length=5, verbose_name='currency char code', unique=True)
    int_code = models.IntegerField(verbose_name='currency unique identifier', unique=True)
    usd_coeff = models.DecimalField(max_digits=12, decimal_places=2, default=1)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


# Product(AbstractModel) with title, content(will be contains html), is published, date published, price,  currency (FK on Currency model)
class Product(AbstractModel):
    name = models.CharField(max_length=400, verbose_name='Product name', unique=True)
    description = models.TextField(null=True, blank=True, verbose_name='Product description')
    is_published = models.BooleanField(default=False)
    date_published = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Product price')
    currency = models.ForeignKey(Currency, verbose_name='currency of product price')   
    objects = ProductManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class CustomUser(AbstractUser):
    timezone = models.CharField(max_length=50, default='Europe/Moscow', verbose_name='User timezone')
    confirmation_code = models.CharField(max_length=128, null=True, blank=True, verbose_name='User URL confirmation code')

    def __unicode__(self):
        return self.username

    def _get_unique_key(self):
        api_key = ApiKey.objects.create(user=self)
        return api_key

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = "Market user"
        verbose_name_plural = "Market users"


class Review(AbstractModel):
    content = models.TextField(verbose_name='Review content')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='annotated product')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True, verbose_name='Author of the review')

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


# Create Ingredient(AbstractModel) with price with M2M on Product (one Product can have a lot of ing and one ing can have a lot of Products)
class Ingredient(AbstractModel):
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=u'Ingredient price')
    name = models.CharField(max_length=400, verbose_name=u'Ingredient')
    products = models.ManyToManyField(Product, related_name='ings', through='Composition', verbose_name=u'Products with this ingredient')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"


class Composition(models.Model):
    ing = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    short_info = models.CharField(max_length=400, null=True, blank=True, verbose_name='notes on use')

    class Meta:
        unique_together = ("ing", "product")


class Order(AbstractModel):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    objects = OrderManager()

    def __unicode__(self):
        return "Order number %s" % str(self.pk)

    class Meta:
        verbose_name = "Customer order"
        verbose_name_plural = "Customer orders"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name='Numbers of product in the order item', default=1)

    class Meta:
        verbose_name = "Order item"
        verbose_name_plural = "Order items"


class OrderMaterializedViewModel(models.Model):
    class Meta:
        db_table = 'showcase_orders_view_m'
        abstract = True

