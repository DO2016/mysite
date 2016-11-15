from tastypie.models import ApiKey

from django.dispatch.dispatcher import Signal

from .models import CustomUser

#{'update_fields': None, 'instance': <CustomUser: SVIN>, 
#'signal': <django.db.models.signals.ModelSignal object at 0x10623e810>,
# 'created': True, 'raw': False, 'using': 'default'}


@receiver(post_save)
def post_save_handler(sender, **kwargs):
    if isinstance(kwargs['instance'], CustomUser) and kwargs['created']:
        user = kwargs['instance']
        ApiKey.objects.create(user=user)

        if not user.password.startswith('pbkdf2_sha256$'):
            user.set_password(user.password)
            user.save()