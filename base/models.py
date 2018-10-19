# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Entidad (models.Model):
	TIPO = (
		('E', 'EMPRESA'),
		('A', 'ASOCIACIÓN'),
	)
	tipo = models.CharField(max_length=1, choices=TIPO, default='E')
	ruc = models.IntegerField()
	razon_social = models.CharField(max_length=255)
	direccion = models.CharField(max_length=255)
	telefono = models.CharField(max_length=255)
	celular = models.CharField(max_length=255)

	def __str__(self):
		return self.razon_social

class PeriodoCirculacion(models.Model):
	TIPO = (
		('1', 'Mayores'),
		('2', 'Menores'),
	)
	razon_social = models.ForeignKey(Entidad)
	resolucion_autorizacion = models.CharField(max_length=255)
	nro_cupos = models.IntegerField()
	ruta_autorizada = models.CharField(max_length=255)
	representante_legal = models.CharField(max_length=255)
	vehiculo = models.CharField(max_length=1, choices=TIPO, default='1')
	fechainicio_periodo = models.DateField()
	fechafin_periodo = models.DateField()

	def __str__(self):
		return self.resolucion_autorizacion

import datetime
class TarjetaCirculacion(models.Model):
	resolucion_autorizacion = models.ForeignKey(PeriodoCirculacion)
	propietario = models.CharField(max_length=255)
	placa = models.CharField(max_length=255)
	clase = models.CharField(max_length=255)
	marca = models.CharField(max_length=255)
	anio_fabricacion = models.IntegerField()
	modelo = models.CharField(max_length=255)
	combustible = models.CharField(max_length=255)
	nro_ruta = models.IntegerField()
	color = models.CharField(max_length=255)
	cilindro = models.CharField(max_length=255)
	ruedas = models.IntegerField()
	nro_motor = models.CharField(max_length=255)
	nro_serie = models.CharField(max_length=255)
	pasajeros = models.IntegerField()
	asientos = models.IntegerField()
	peso_seco = models.IntegerField()
	peso_bruto = models.IntegerField()
	frecuencia = models.CharField(max_length=255)
	origen = models.CharField(max_length=255)
	poliza_seguro = models.CharField(max_length=255)
	fecha_expedicion = models.DateField()
	fecha = models.DateField()

	class Meta:
		verbose_name_plural='Tarjetas'

class Autoridad(models.Model):
    nombre_autoridad = models.CharField(max_length=255)
    fecha_inicio_autoridad = models.DateField()
    fecha_inicio_autoridad = models.DateField()
    firma_autoridad = models.ImageField(upload_to='firmas_autoridad', max_length=100)
    activo = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='Autoridades'

    def __str__(self):
        return  self.nombre_autoridad
