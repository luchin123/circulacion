# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from base.models import Entidad, PeriodoCirculacion, TarjetaCirculacion

admin.site.register(Entidad)
admin.site.register(PeriodoCirculacion)
admin.site.register(TarjetaCirculacion)
