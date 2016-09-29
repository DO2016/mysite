from django.contrib import admin

# Register your models here.

from .models import Currency, Item, Review, Ingredient, CustomUser

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'is_published', 'date_published', 'price', 'currency')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('price', 'name', )

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'last_name', 'timezone')

# Demonstrates 2 ways of registering:
#admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Ingredient, IngredientAdmin)
