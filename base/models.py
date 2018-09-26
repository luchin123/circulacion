# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Administracion (models.Model):
	nro_documento = models.CharField(max_length=8, unique=True)
	nombre = models.CharField(max_length=255)
	direccion = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	telefono = models.CharField(max_length=255)
	logo = models.ImageField(upload_to='logo', max_length=100)

	def __str__(self):
		return  self.nombre

class Entidad (models.Model):
	TIPO = (
		('E', 'EMPRESA'),
		('A', 'ASOCIACIÓN'),
	)
	tipo = models.CharField(max_length=1, choices=TIPO, default='EMPRESA')
	ruc = models.IntegerField()
	razon_social = models.CharField(max_length=255)
	direccion = models.CharField(max_length=255)
	telefono = models.CharField(max_length=255)
	celular = models.CharField(max_length=255)
	administracion = models.ForeignKey(Administracion)

	def __str__(self):
		return self.razon_social

class Periodo_Circulacion(models.Model):
	TIPO = (
		('M', 'Mayores'),
		('N', 'Menores'),
	)
	razon_social = models.ForeignKey(Entidad)
	resolucion_autorizacion = models.CharField(max_length=255)
	nro_cupos = models.IntegerField()
	ruta_autorizada = models.CharField(max_length=255)
	representante_legal = models.CharField(max_length=255)
	vehiculo = models.CharField(max_length=1, choices=TIPO, default='Mayores')
	fechainicio_periodo = models.DateField()
	fechafin_periodo = models.DateField()

	def __str__(self):
		return self.resolucion_autorizacion

import datetime
class Tarjeta_Circulacion(models.Model):
	CLASES = (
		('A', 'A'),
		('B', 'B'),
		('C', 'C'),
	)
	resolucion_autorizacion = models.ForeignKey(Periodo_Circulacion)
	propietario = models.CharField(max_length=255)
	placa = models.CharField(max_length=255)
	clase = models.CharField(max_length=1, choices=CLASES, default='A')
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


# Create your models here.
