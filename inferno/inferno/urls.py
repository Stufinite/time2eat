"""inferno URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from infernoWeb.view import inferno
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', inferno.index, name='inferno'),
    url(r'^admin/', admin.site.urls),
    url(r'^infernoWeb/',include('infernoWeb.urls',namespace="infernoWeb") ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

import slothTw.urls
urlpatterns += [
    url(r'^sloth/',include(slothTw.urls, namespace="sloth") ),
]

import arrogant.urls
urlpatterns += [
    url(r'^arrogant/',include(arrogant.urls, namespace="arrogant") ),
]


urlpatterns += [
    url(r'^greed$', TemplateView.as_view(template_name='greed/index.html')), 
    url(r'^greed/inside$', TemplateView.as_view(template_name='greed/inside.html')), 
]

# videoDemo
urlpatterns += [
    url(r'^videoDemo/',include("videoDemo.urls", namespace="videoDemo") ),
]
