from tastypie.admin import ApiKeyInline

from django.contrib import admin

from .forms import IngredientAdminForm
from .models import Currency, Product, Review, Ingredient, CustomUser, Order, OrderItem, Composition


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_published', 'date_published', 'price', 'currency', 'get_ings')

    def get_ings(self, obj):
        return "\n".join(list(obj.ings.all().values_list('name'), flat=True)) 


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', 'product', 'author',)

    fieldsets = (
    (None, {
        'fields': ('content', )
    }),)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_products',)
    search_fields = ['name', 'price',]
    list_filter = ('name', 'price',)
    ordering = ['-name']
    filter_vertical = ('products',)
    form = IngredientAdminForm

    def get_products(self, obj):
        return "\n".join(list(obj.products.all().values_list('name'), flat=True)) 


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ('short_info', 'product_id', 'ing_id')


class OrderStackedInline(admin.StackedInline):
    model = Order


class ReviewTabularInline(admin.TabularInline):
    model = Review


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'last_name', 'timezone',)
    # Appropriate link: ForeignKey ; Not appropriate link: ManyToMany 
    inlines = [ApiKeyInline, ReviewTabularInline, OrderStackedInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', ]
