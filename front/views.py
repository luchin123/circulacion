# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from base.models import *
from base.forms import EntidadForm, Periodo_CirculacionForm, Tarjeta_CirculacionForm

from front.utils import crear_enlace, timestamp_a_fecha

from collections import OrderedDict
import json
# Create your views here.

def the_login(request):
    if(request.user.is_authenticated()):
        return HttpResponseRedirect(reverse('front:index'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('front:index'))
            else:
                messages.warning(request, 'El usuario no está activo.')
        else:
            messages.warning(request, 'Revise el usuario o la contraseña.')
        

    return render(request, 'front/login.html')

def consulta(request):
    return render(request, 'front/consulta-lista.html')

def consulta_json(request):
    filters = []
    cols = []
    for k in request.GET:
        if 'filter[' in k:
            filters.append(k)
        if 'column[' in k:
            cols.append(k)

    size = int(request.GET.get('size'))
    page = int(request.GET.get('page'))

    limit = page * size
    offset = limit + size

    data = {
        'headers': [
            'Resolucion', 'Propietario', 'Placa', 'Clase', 'Marca', 'Fabricacion', 'Modelo','Ruta','Pasajeros','Poliza','Fecha Exp','Fecha' 'Acciones'
        ]

    }

    tarjetas = Tarjeta_Circulacion.objects.all().order_by('-pk')

    if 'filter[0]' in filters:
        tarjetas = tarjetas.filter(periodo_Circulacion__resolucion_autorizacion__contains = request.GET.get('filter[0]'))

    if 'filter[1]' in filters:
        tarjetas = tarjetas.filter(propietario__icontains = request.GET.get('filter[1]'))

    if 'filter[2]' in filters:
        tarjetas = tarjetas.filter(placa__icontains = request.GET.get('filter[2]'))

    if 'filter[3]' in filters:
        tarjetas = tarjetas.filter(clase__icontains = request.GET.get('filter[3]'))

    if 'filter[4]' in filters:
        tarjetas = tarjetas.filter(Marca = request.GET.get('filter[4]'))

    if 'filter[5]' in filters:
        tarjetas = tarjetas.filter(fabricacion = request.GET.get('filter[5]'))

    if 'filter[6]' in filters:
        tarjetas = tarjetas.filter(modelo = request.GET.get('filter[6]'))

    if 'filter[7]' in filters:
        tarjetas = tarjetas.filter(ruta = request.GET.get('filter[8]'))

    if 'filter[8]' in filters:
        tarjetas = tarjetas.filter(pasajeros = request.GET.get('filter[10]'))

    if 'filter[9]' in filters:
        tarjetas = tarjetas.filter(poliza = request.GET.get('filter[12]'))

    if 'filter[10]' in filters:
        str_fecha = request.GET.get('filter[13]')
        if str_fecha[:2] == '<=':
            fecha = str_fecha[2:12]
            tarjetas = tarjetas.distinct().filter(fecha_expedicion__lte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        elif str_fecha[:2] == '>=':
            fecha = str_fecha[2:12]
            tarjetas = tarjetas.distinct().filter(fecha_expedicion__gte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        else:
            inicial = timestamp_a_fecha(str_fecha[:10], '%Y-%m-%d')
            final = timestamp_a_fecha(str_fecha[-13:][:10], '%Y-%m-%d')
            tarjetas = tarjetas.distinct().filter(fecha_expedicion__range = (inicial, final))

    if 'filter[11]' in filters:
        str_fecha = request.GET.get('filter[14]')
        if str_fecha[:2] == '<=':
            fecha = str_fecha[2:12]
            tarjetas = tarjetas.distinct().filter(fecha__lte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        elif str_fecha[:2] == '>=':
            fecha = str_fecha[2:12]
            tarjetas = tarjetas.distinct().filter(fecha__gte = timestamp_a_fecha(fecha, '%Y-%m-%d'))
        else:
            inicial = timestamp_a_fecha(str_fecha[:10], '%Y-%m-%d')
            final = timestamp_a_fecha(str_fecha[-13:][:10], '%Y-%m-%d')
            tarjetas = tarjetas.distinct().filter(fecha__range = (inicial, final))
    

    if 'column[0]' in cols:
        signo = '' if request.GET.get('column[0]') == '0' else '-'
        tarjetas = tarjetas.order_by('%sresolucion_autorizacion' % signo)

    if 'column[1]' in cols:
        signo = '' if request.GET.get('column[1]') == '0' else '-'
        tarjetas = tarjetas.order_by('%spropietario' % signo)

    if 'column[2]' in cols:
        signo = '' if request.GET.get('column[2]') == '0' else '-'
        tarjetas = tarjetas.order_by('%splaca' % signo)

    if 'column[3]' in cols:
        signo = '' if request.GET.get('column[3]') == '0' else '-'
        tarjetas = tarjetas.order_by('%sclase' % signo)

    if 'column[4]' in cols:
        signo = '' if request.GET.get('column[4]') == '0' else '-'
        tarjetas = tarjetas.order_by('%smarca' % signo)

    if 'column[5]' in cols:
        signo = '' if request.GET.get('column[5]') == '0' else '-'
        tarjetas = tarjetas.order_by('%sfabricacion' % signo)

    if 'column[6]' in cols:
        signo = '' if request.GET.get('column[6]') == '0' else '-'
        tarjetas = tarjetas.order_by('%smodelo' % signo)

    if 'column[7]' in cols:
        signo = '' if request.GET.get('column[8]') == '0' else '-'
        tarjetas = tarjetas.order_by('%sruta' % signo)

    if 'column[8]' in cols:
        signo = '' if request.GET.get('column[10]') == '0' else '-'
        tarjetas = tarjetas.order_by('%spasajeros' % signo)

    if 'column[9]' in cols:
        signo = '' if request.GET.get('column[12]') == '0' else '-'
        tarjetas = tarjetas.order_by('%spoliza' % signo)

    if 'column[10]' in cols:
        signo = '' if request.GET.get('column[13]') == '0' else '-'
        tarjetas = tarjetas.order_by('%sfecha_expedicion' % signo)

    if 'column[11]' in cols:
        signo = '' if request.GET.get('column[14]') == '0' else '-'
        tarjetas = tarjetas.order_by('%sfecha' % signo)

    total_rows = tarjetas.count()

    tarjetas = tarjetas[limit:offset]

    rows = []
    for tarjeta in tarjetas:

        links = crear_enlace(reverse('front:tarjeta', args=[tarjeta.id]), 'success', 'Ver o Editar', 'edit')
       # -*- links += crear_enlace(reverse('reporte:licencia_print', args=[licencia.id]), 'success', 'Imprimir Anverso', 'print')
       # -*-links += crear_enlace(reverse('reporte:licencia_print2', args=[licencia.id]), 'info', 'Imprimir Reverso', 'print')

        obj = OrderedDict({
            '0': tarjeta.periodo_circulacion.resolucion,
            '1': tarjeta.propietario,
            '2': tarjeta.placa,
            '3': tarjeta.clase,
            '4': tarjeta.marca,
            '5': tarjeta.fabricacion,
            '6': tarjeta.modelo,
            '7': tarjeta.ruta,
            '8': tarjeta.pasajeros,
            '9': tarjeta.poliza,
            '10': tarjeta.fecha_expedicion.strftime('%d/%b/%Y'),
            '11': tarjeta.fecha.strftime('%d/%b/%Y'),
            '12': links,
        })
        rows.append(obj)

    data['rows'] = rows
    data['total_rows'] = total_rows

    return HttpResponse(json.dumps(data), content_type = "application/json")

@login_required
def index(request):
    return render(request, 'front/index.html')

@login_required
def tarjeta(request, id=None):
    l=None
    if id is not None:
        l=Tarjeta_Circulacion.objects.get(id=id)
    if request.method == 'POST':
        if l is None:
            form = Tarjeta_CirculacionForm(request.POST)
        else:
            form = Tarjeta_CirculacionForm(request.POST,instance=l)
        if form.is_valid():
            tarjeta = form.save(commit=False)
            periodo_circulacion = request.POST.get('periodo_circulacion')
            periodo_circulacion = periodo_circulacion.objects.get(id = periodo_circulacion)
            tarjeta.periodo_circulacion = periodo_circulacion
            tarjeta.save()
            if l is None:
                messages.warning(request, 'Se ha creado una tarjeta.')
            else:
                messages.warning(request, 'Se ha Actualizado una tarjeta.')
            return HttpResponseRedirect(reverse('front:consulta'))
        else:
            return render(request, 'front/tarjeta.html', {'form': form})
    else:
        if l is None:
            form = Tarjeta_CirculacionForm()   
        else:
            form = Tarjeta_CirculacionForm(instance=l)
        return render(request, 'front/tarjeta.html', {'form': form})

@login_required
def empresas(request):
    return render(request, 'front/entidad-lista.html')

def empresas_json(request):
    filters = []
    cols = []
    for k in request.GET:
        if 'filter[' in k:
            filters.append(k)
        if 'column[' in k:
            cols.append(k)

    size = int(request.GET.get('size'))
    page = int(request.GET.get('page'))

    limit = page * size
    offset = limit + size

    data = {
        'headers': [
            'Tipo', 'Ruc', 'Razon Social', 'Direccion', 'Telefono','Celular','Administracion', 'Acciones'
        ]

    }

    empresas = Entidad.objects.all().order_by('-pk')

    if 'filter[0]' in filters:
        tipo_reverse = dict((v,k) for k, v in Entidad.TIPO)
        empresas = empresas.filter(tipo = tipo_reverse[request.GET.get('filter[0]')])

    if 'filter[1]' in filters:
        empresas = empresas.filter(ruc__icontains = request.GET.get('filter[1]'))

    if 'filter[2]' in filters:
        empresas = empresas.filter(razon_social__icontains = request.GET.get('filter[2]'))

    if 'filter[3]' in filters:
        empresas = empresas.filter(direccion__icontains = request.GET.get('filter[3]'))

    if 'filter[4]' in filters:
        empresas = empresas.filter(telefono__icontains = request.GET.get('filter[4]'))

    if 'filter[5]' in filters:
        empresas = empresas.filter(celular__icontains = request.GET.get('filter[5]'))

    if 'filter[6]' in filters:
        empresas = empresas.filter(administracion__icontains = request.GET.get('filter[6]'))

    

    if 'column[0]' in cols:
        signo = '' if request.GET.get('column[0]') == '0' else '-'
        empresas = empresas.order_by('%stipo' % signo)

    if 'column[1]' in cols:
        signo = '' if request.GET.get('column[1]') == '0' else '-'
        empresas = empresas.order_by('%sruc' % signo)

    if 'column[2]' in cols:
        signo = '' if request.GET.get('column[2]') == '0' else '-'
        empresas = empresas.order_by('%srazon_social' % signo)

    if 'column[3]' in cols:
        signo = '' if request.GET.get('column[3]') == '0' else '-'
        empresas = empresas.order_by('%sdireccion' % signo)

    if 'column[4]' in cols:
        signo = '' if request.GET.get('column[4]') == '0' else '-'
        empresas = empresas.order_by('%stelefono' % signo)

    if 'column[5]' in cols:
        signo = '' if request.GET.get('column[5]') == '0' else '-'
        empresas = empresas.order_by('%scelular' % signo)

    if 'column[6]' in cols:
        signo = '' if request.GET.get('column[6]') == '0' else '-'
        empresas = empresas.order_by('%sadministracion' % signo)


    total_rows = empresas.count()

    empresas = empresas[limit:offset]

    rows = []
    for entidad in empresas:

        links = crear_enlace(reverse('front:empresa', args=[entidad.id]), 'success', 'Ver o Editar', 'edit')
        links += crear_enlace(reverse('front:resoluciones_entidad', args=[entidad.id]), 'danger', 'Ver Resoluciones', 'ban')

        obj = OrderedDict({
            '0': entidad.get_tipo_display(),
            '1': entidad.ruc,
            '2': entidad.razon_social,
            '3': entidad.direccion,
            '4': entidad.telefono,
            '5': entidad.celular,
            '6': entidad.administracion.nombre,
            '7': links,
        })
        rows.append(obj)

    data['rows'] = rows
    data['total_rows'] = total_rows

    return HttpResponse(json.dumps(data), content_type = "application/json")

@login_required
def empresa(request, id=None):
    p=None
    if id is not None:
        p=Entidad.objects.get(id=id)
    if request.method == 'POST':
        if p is None:
            form = EntidadForm(request.POST, request.FILES)
        else:
            form = EntidadForm(request.POST,request.FILES,instance=p)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.save()
            if p is None:
                messages.warning(request, 'Se ha creado una Empresa.')
            else:
                messages.warning(request, 'Se ha Actualizado una Emoresa.')
            return HttpResponseRedirect(reverse('front:empresas'))
        else:
            return render(request, 'front/entidad.html', {'form': form})
    else:
        if p is None:
            form = EntidadForm()   
        else:
            form = EntidadForm(instance=p)
        return render(request, 'front/entidad.html', {'form': form})

@login_required
def resolucion_entidad(request, id_entidad, id):
    entidad=Entidad.objects.get(id=id_entidad)
    s = None
    if id != '0':
        s = Periodo_Circulacion.objects.get(id=id)
    if s is None:
        form = Periodo_CirculacionForm()
    else:
        form = Periodo_CirculacionForm(instance=s)
    if request.method == 'POST':
        if s is None:
            form = Periodo_CirculacionForm(request.POST)
        else:
            form = Periodo_CirculacionForm(request.POST, instance=s)

        if form.is_valid():
            resolucion = form.save(commit=False)
            resolucion.razon_social=entidad
            resolucion.save()
            if s is None:
                messages.warning(request, 'Se ha creado una resolucion para %s.' % entidad)
            else:
                messages.warning(request, 'Se ha actualizado una Resolucion para %s.' % entidad)
            return HttpResponseRedirect(reverse('front:personas'))
        else:
            return render(request, 'front/resolucion.html', {'form': form, 'entidad':entidad})
    else:
        return render(request, 'front/resolucion.html', {'form': form, 'entidad':entidad})


@login_required
def resoluciones_entidad(request, entidad_id):
    entidad=Entidad.objects.get(id=entidad_id)
    return render(request, 'front/lista-resoluciones.html', {'entidad':entidad})