# -*- coding: utf-8 -*-

from xlsxwriter.workbook import Workbook
try:
	import cStringIO as StringIO
except ImportError:
	import StringIO
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from base.models import Entidad, TarjetaCirculacion
from django.contrib.auth.decorators import login_required

@login_required()
def vehiculos_excel(request, id):
	output = StringIO.StringIO()

	book = Workbook(output)
	sheet = book.add_worksheet(u'Vehículos')

	titulo = book.add_format({
		'bold': 1,
		'align': 'center'
		})

	negrita = book.add_format({'bold': 1})

	empresa = get_object_or_404(Entidad, pk = id)

	hasta = 'I'
	sheet.merge_range('A1:%s1' % hasta, 'Municipalidad de Provincial de Urubamba', titulo)
	sheet.merge_range('A2:%s2' % hasta, 'Listado de Vehiculos', titulo)
	sheet.merge_range('A3:%s3' % hasta, empresa.razon_social, titulo)

	sheet.write('A5', 'Propietario', negrita)
	sheet.write('B5', 'Placa', negrita)
	sheet.write('C5', 'Clase', negrita)
	sheet.write('D5', 'Marca', negrita)
	sheet.write('E5', 'Año Fabricacion', negrita)
	sheet.write('F5', 'Modelo', negrita)
	sheet.write('G5', 'Ruta', negrita)
	sheet.write('H5', 'Pasajeros', negrita)
	sheet.write('I5', 'Poliza', negrita)


	tarjetas = TarjetaCirculacion.objects.filter(resolucion_autorizacion__razon_social__id = empresa.id)

	fila = 6
	for tarjeta in tarjetas:
		sheet.write('A%s' % fila, tarjeta.propietario)
		sheet.write('B%s' % fila, tarjeta.placa)
		sheet.write('C%s' % fila, tarjeta.clase)
		sheet.write('D%s' % fila, tarjeta.marca)
		sheet.write('E%s' % fila, tarjeta.anio_fabricacion)
		sheet.write('F%s' % fila, tarjeta.modelo)
		sheet.write('G%s' % fila, tarjeta.nro_ruta)
		sheet.write('H%s' % fila, tarjeta.pasajeros)
		sheet.write('I%s' % fila, tarjeta.poliza_seguro)
		fila += 1

	sheet.autofilter('A5:%s%s' % (hasta, fila))
	book.close()

	output.seek(0)

	response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment; filename=vehiculos-%s.xlsx" % str(empresa.ruc)

	return response
