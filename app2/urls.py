from django.conf.urls import url

from . import views

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login_view, name='login_view'),
    url(r'^logout$', views.logout_view, name='logout_view'),
    url(r'^profile/(?P<pk>\d+)/$', views.profile_view, name='profile_view'),
    url(r'^profile/', views.profile_view, name='profile_view'),
    url(r'^register$', views.registration_view, name='registration_view'),
    url(r'^confirm/(?P<confirmation_code>\w{33})/(?P<username>\w+)$', views.confirm_view, name='confirm_view'),
]