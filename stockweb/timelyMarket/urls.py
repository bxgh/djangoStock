"""stockweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based viewscd
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url
from . import views as tmv


urlpatterns = [    
    # path('index/', tmv.index),
    path('stockMarket/', tmv.stockMarket),
    path('klinedata/', tmv.klineData),
    path('mlineData/', tmv.mlineData),
    path('stockStaticData/', tmv.stockStaticData),
    path('test_websocket/', tmv.test_websocket),
    path('stockmline_ws/', tmv.stockmline_ws),
    url(r'^index/', tmv.index),
]
