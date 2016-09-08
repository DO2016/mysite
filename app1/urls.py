from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$', views.article_detail, name='article_detail'),
    url(r'^articles/(\d{4})/(\d{2})/$', views.month_archive, name='month_archive'),
    url(r'^table', views.index_table, name='index_table'),
    url(r'^$', views.index, name='index'),
]