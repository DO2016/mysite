"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles import views

from showcase.api import v1_api

urlpatterns = [
    url(r'^showcase/', include('showcase.urls', namespace='showcase')),
    url(r'^admin/', admin.site.urls),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS

    url(r'^api/v1/doc/',
      include('tastypie_swagger.urls', namespace='myapi_tastypie_swagger'),
      kwargs={"tastypie_api_module" : "showcase.api.v1_api", "namespace" : "myapi_tastypie_swagger", "version" : "0.1"}
    ),
    url(r'^api/', include(v1_api.urls)), # tastypie URLS
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
