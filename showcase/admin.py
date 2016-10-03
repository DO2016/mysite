from django.contrib import admin

# Register your models here.

from .models import Currency, Product, Review, Ingredient, CustomUser

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_published', 'date_published', 'price', 'currency')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('price', 'name', )


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'last_name', 'timezone')
