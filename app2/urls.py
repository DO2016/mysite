from django.conf.urls import url

from . import views

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_view, name='login_view'),
    url(r'^logout$', views.logout, name='logout'),
]