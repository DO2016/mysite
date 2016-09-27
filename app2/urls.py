from django.conf.urls import url
from . import views
from django.views import View
from django.contrib import admin
from .views import *
from django.contrib.auth.decorators import login_required

admin.autodiscover()

#urlpatterns = [
#    url(r'^about/$', MyView.as_view()),
#]

urlpatterns = [
    url(r'^$', login_required(IndexView.as_view()), name='index'),
    url(r'^login', LoginView.as_view(), name='login_view'),
    url(r'^logout$', LogoutView.as_view()),
    url(r'^profile/(?P<pk>\d+)/$', ProfileView.as_view()),
    url(r'^profile/', ProfileView.as_view()),
    url(r'^register$', RegistrationView.as_view()),
    url(r'^confirm/(?P<confirmation_code>\w{33})/(?P<username>\w+)$', ConfirmationView.as_view()),

    url(r'^items/$', ItemListView.as_view(), name='itemlist_view'),
    url(r'^details/(?P<pk>[-\w]+)', ItemDetail.as_view(), name='itemdetail_view'),
    url(r'^details/', ItemDetail.as_view(), name='detail_template'),
]
