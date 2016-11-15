from tastypie.models import ApiKey
from tastypie.utils import trailing_slash
from tastypie.authentication import Authentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.api import Api

from .models import Product, Ingredient, CustomUser, Order, OrderItem, Currency


class RegistrationAuthorization(Authorization):
    pass


class BackboneCompatibleResource(ModelResource):
    class Meta:
        always_return_data = True


class AuthenticationResource(BackboneCompatibleResource):
    def obj_get_list(self, bundle, **kwargs):
        print "**** obj_get_list"
        qs = super(AuthenticationResource, self).obj_get_list(bundle, **kwargs)
        return qs.filter(user=bundle.request.user)

    class Meta(BackboneCompatibleResource.Meta):
        queryset = ApiKey.objects.all()
        fields = ['key', 'user']
        allowed_methods_list = ['get']
        resource_name = 'AuthenticationResource'
        authentication = BasicAuthentication()


class RegistrationResource(BackboneCompatibleResource):

    class Meta(BackboneCompatibleResource.Meta):
        queryset = CustomUser.objects.all()
        fields = []
        allowed_methods_list = ['post']
        resource_name = 'RegistrationResource'
        authentication = Authentication()
        authorization = RegistrationAuthorization()


class ProductResource(BackboneCompatibleResource):
    class Meta:
        resource_name = 'ProductResource'
        excludes = ['description']
        authentication = ApiKeyAuthentication()
        # authorization = 

    def dehydrate(self, bundle):
        bundle.data['full_name'] = 'Showcase market product sample.'
        return bundle

    def hydrate_profile(self, bundle):
        bundle.data['full_name'] = bundle.obj.profile
        return bundle


class IngredientResource(BackboneCompatibleResource):
    class Meta:
        queryset = Ingredient.objects.all()
        resource_name = 'IngredientResource'
        authentication = ApiKeyAuthentication()
        # authorization = 


class CustomUserResource(BackboneCompatibleResource):
    class Meta:
        queryset = CustomUser.objects.all()
        resource_name = 'CustomUserResource'
        authentication = ApiKeyAuthentication()


class OrderResource(BackboneCompatibleResource):
    class Meta:
        queryset = Order.objects.all()
        resource_name = 'OrderResource'
        authentication = ApiKeyAuthentication()


class OrderItemResource(BackboneCompatibleResource):
    class Meta:
        queryset = OrderItem.objects.all()
        resource_name = 'OrderItemResource'
        authentication = BasicAuthentication()


class OrderResource(ModelResource):
    class Meta:
        queryset = Order.objects.all()
        resource_name = 'OrderResource'
        authentication = BasicAuthentication()


class CurrencyResource(ModelResource):
    class Meta:
        queryset = Currency.objects.all()
        resource_name = 'CurrencyResource'
        authentication = BasicAuthentication()


v1_api = Api(api_name='v1')
v1_api.register(ProductResource())
v1_api.register(IngredientResource())
v1_api.register(CustomUserResource())
v1_api.register(CurrencyResource())
v1_api.register(AuthenticationResource())
