# -*- coding: utf-8 -*-

from django.conf.urls import url

from reporte import views, excel

app_name = 'reporte'
urlpatterns = [
  
    url(r'^imprimir/tarjeta/(?P<id>.*)$', views.tarjeta_print, name = 'tarjeta_print'),
    url(r'^imprimir/pdf/(?P<id>.*)$', views.vehiculos_pdf, name = 'vehiculos_pdf'),
    url(r'^imprimir/excel/(?P<id>.*)$', excel.vehiculos_excel, name = 'vehiculos_excel'),


]
