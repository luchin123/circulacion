# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from base.models import Administracion, Entidad, Periodo_Circulacion, Tarjeta_Circulacion
admin.site.register(Administracion)
admin.site.register(Entidad)
admin.site.register(Periodo_Circulacion)
admin.site.register(Tarjeta_Circulacion)