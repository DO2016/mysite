from tastypie.models import ApiKey

from django.db.models.signals import post_save
from django.dispatch.dispatcher import Signal
from django.dispatch import receiver

from .models import CustomUser

#{'update_fields': None, 'instance': <CustomUser: SVIN>, 
#'signal': <django.db.models.signals.ModelSignal object at 0x10623e810>,
# 'created': True, 'raw': False, 'using': 'default'}


@receiver(post_save)
def post_save_handler(sender, **kwargs):
    if isinstance(kwargs['instance'], CustomUser) and kwargs['created']:
        user = kwargs['instance']

        if not user.password.startswith('pbkdf2_sha256$'):        
            ApiKey.objects.create(user=user)
            user.set_password(user.password)
            user.save()