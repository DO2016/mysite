from tastypie.resources import ModelResource
from .models import Product, Ingredient, CustomUser

# Add custom field “name” for resource Item and implement dehydrate, hydrate for handling it (just get title, and save to title). Exclude title
class ProductResource(ModelResource):
    full_name = fields.CharField(max_length=256, unique=True)

    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product'

    def dehydrate_full_name(self, bundle):
        return bundle.obj.data.full_name.upper()


class IngredientResource(ModelResource):
    class Meta:
        queryset = Ingredient.objects.all()
        resource_name = 'ingredient'


class CustomUserResource(ModelResource):
    class Meta:
        queryset = CustomUser.objects.all()
        resource_name = 'custom_user'