from django.conf.urls import include, url
from . import views
from django.views import View
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy, resolve


admin.autodiscover()


urlpatterns = [
    url(r'', views.IndexView.as_view(), name='index'),
]
