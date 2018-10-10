# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'periodos', views.PeriodoCirculacionViewSet)

app_name = 'base'
urlpatterns = [

    url(r'^api/base/', include(router.urls)),
    url(r'^api/base/periodo/filter/$', views.PeriodoCirculacionFilterViewSet.as_view()),

]
