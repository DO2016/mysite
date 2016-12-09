from django.conf.urls import include, url
from . import views
from django.views import View
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy, resolve


admin.autodiscover()


urlpatterns = [
    url(r'', views.IndexView.as_view(), name='index'),
    #url(r'^$', login_required(views.IndexView.as_view(), login_url=reverse_lazy("showcase:login")), name='index'),
    #url(r'^login', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^register$', views.RegistrationView.as_view(), name='register'),
    url(r'^confirm/(?P<confirmation_code>[-\w]+)/(?P<username>[-\w]+)$', views.ConfirmationView.as_view(), name='confirm' ),
    url(r'^products/', login_required(views.ProductListView.as_view(), login_url=reverse_lazy("showcase:login")), name='products'),
    url(r'^details/(?P<pk>[-\w]+)', login_required(views.ProductDetail.as_view()), name='details'),
]
