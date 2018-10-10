# -*- coding: utf-8 -*-

from django.conf.urls import url

from reporte import views

app_name = 'reporte'
urlpatterns = [
  
    url(r'^imprimir/tarjeta/(?P<id>.*)$', views.tarjeta_print, name = 'tarjeta_print'),

]
