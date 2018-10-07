# -*- coding: utf-8 -*-

from django.conf.urls import url

from front import views

app_name = 'front'
urlpatterns = [

	url(r'^$', views.index, name = 'index'),
	url(r'^login/$', views.the_login, name = 'login'),
	url(r'^consulta/$', views.consulta, name = 'consulta'),
    url(r'^consultas/json/$', views.consulta_json, name = 'consulta_json'),
    url(r'^empresas/$', views.empresas, name = 'empresas'),
    url(r'^empresas/json/$', views.empresas_json, name = 'empresas_json'),
    url(r'^empresa/$', views.empresa, name = 'empresa'),
    url(r'^resolucion/(?P<id_entidad>.*)/(?P<id>.*)$', views.resolucion_entidad, name = 'resolucion_entidad'),
    url(r'^resoluciones/(?P<_id>.*)$', views.resoluciones_entidad, name = 'resoluciones_entidad'),
]