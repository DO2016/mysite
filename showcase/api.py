import django_rq

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _ul

from tastypie.api import Api
from tastypie import fields, utils
from tastypie.models import ApiKey
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication, ApiKeyAuthentication, BasicAuthentication

from .tasks import create_rnd_sales
from .models import Product, Ingredient, CustomUser, Order, OrderItem, Currency, Review
from .signals import post_save_handler

post_save.connect(post_save_handler)

class RegistrationAuthorization(Authorization):
    pass


class BackboneCompatibleResource(ModelResource):
    class Meta:
        always_return_data = True


class ConfirmationResource(BackboneCompatibleResource):
    api_key = fields.ToOneField('showcase.api.ApiKeyResource', 'api_key', full=True)

    def obj_get_list(self, bundle, **kwargs):
        qs = super(ConfirmationResource, self).obj_get_list(bundle, **kwargs)
        key = bundle.request.META['HTTP_APIKEY']
        user_name = bundle.request.META['HTTP_USERNAME']
        qs = qs.filter(username=user_name)
        if key == qs[0].api_key.key:
            mdl = qs.get(username=user_name)
            mdl.is_active = True
            mdl.save()
            return qs

    class Meta(BackboneCompatibleResource.Meta):
        queryset = CustomUser.objects.all()
        allowed_methods_list = ['get', 'post']
        resource_name = 'ConfirmationResource'


class ApiKeyResource(BackboneCompatibleResource):
    user = fields.ToOneField('showcase.api.ConfirmationResource', 'user')

    class Meta(BackboneCompatibleResource.Meta):
        queryset = ApiKey.objects.all()
        fields = ['key', 'user']
        allowed_methods_list = ['get']
        resource_name = 'ApiKeyResource'


class AuthenticationResource(BackboneCompatibleResource):
    def obj_get_list(self, bundle, **kwargs):
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


class CurrencyResource(ModelResource):
    class Meta(BackboneCompatibleResource.Meta):
        queryset = Currency.objects.all()
        resource_name = 'CurrencyResource'
        authentication = ApiKeyAuthentication()


class ProductResource(BackboneCompatibleResource):
    reviews = fields.ToManyField('showcase.api.ReviewResource', 'reviews', related_name='product', blank=True, null=True, full=True)
    currency = fields.ForeignKey(CurrencyResource, 'currency')
    allowed_methods_list = ['get']
    #sum_ings_price = fields.DecimalField(readonly=True)

    class Meta(BackboneCompatibleResource.Meta):
        queryset = Product.objects.all_published()
        resource_name = 'ProductResource'        
        authorization = Authorization()

    #def dehydrate_sum_ings_price(self, bundle):
    #    return bundle.obj.sum_ings_price


class AddProductResource(BackboneCompatibleResource):
    reviews = fields.ToManyField('showcase.api.ReviewResource', 'reviews', related_name='product', blank=True, null=True, full=True)
    currency = fields.ForeignKey(CurrencyResource, 'currency')
    allowed_methods_list = ['post']

    class Meta(BackboneCompatibleResource.Meta):
        queryset = Product.objects.all_published()
        resource_name = 'AddProductResource'        
        authentication = ApiKeyAuthentication()
        authorization = Authorization()


class ReviewResource(BackboneCompatibleResource):
    product = fields.ToOneField(ProductResource, 'product')
    class Meta(BackboneCompatibleResource.Meta):
        queryset = Review.objects.all()


class IngredientResource(BackboneCompatibleResource):
    class Meta(BackboneCompatibleResource.Meta):
        queryset = Ingredient.objects.all()
        resource_name = 'IngredientResource'
        authentication = ApiKeyAuthentication()


class CustomUserResource(BackboneCompatibleResource):
    class Meta(BackboneCompatibleResource.Meta):
        queryset = CustomUser.objects.all()
        resource_name = 'CustomUserResource'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def _send_email(self, bundle, user):
        token_url = "%s://%s/#confirm/%s/%s/" % (
            bundle.request.scheme, 
            bundle.request.get_host(),
            user.api_key.key,
            user.username
        )
        send_mail(
            _ul(u'Account confirmation'), 
            _ul(u'Go to %s for complete registration') % token_url, 
            settings.EMAIL_HOST_USER,
            [user.email], 
            fail_silently=False
        )

    def obj_create(self, bundle, **kwargs):
        res = super(CustomUserResource, self).obj_create(bundle, **kwargs)
        #import ipdb as pdb; pdb.set_trace()
        self._send_email(bundle, bundle.obj)
        return res


class OrderResource(BackboneCompatibleResource):
    class Meta(BackboneCompatibleResource.Meta):
        queryset = Order.objects.all()
        resource_name = 'OrderResource'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()


class OrderItemResource(BackboneCompatibleResource):
    class Meta(BackboneCompatibleResource.Meta):
        queryset = OrderItem.objects.all()
        resource_name = 'OrderItemResource'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()


class OrderResource(ModelResource):
    class Meta(BackboneCompatibleResource.Meta):
        queryset = Order.objects.all()
        resource_name = 'OrderResource'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()


class GenerationResource(ModelResource):
    def obj_get_list(self, bundle, **kwargs):
        print "start RQ-job here..."
        django_rq.enqueue(create_rnd_sales, None, None)
        return super(GenerationResource, self).obj_get_list(bundle, **kwargs);

    class Meta(BackboneCompatibleResource.Meta):
        resource_name = 'GenerationResource'
        queryset = OrderItem.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = Authorization()



v1_api = Api(api_name='v1')
v1_api.register(ProductResource())
v1_api.register(AddProductResource())
v1_api.register(IngredientResource())
v1_api.register(CustomUserResource())
v1_api.register(CurrencyResource())
v1_api.register(AuthenticationResource())
v1_api.register(ConfirmationResource())
v1_api.register(GenerationResource())

