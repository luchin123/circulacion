# -*- coding: utf-8 -*-

from django.forms import ModelForm, TextInput, Select, Textarea, DateField, CheckboxInput, FileInput

from models import Entidad, PeriodoCirculacion, TarjetaCirculacion
from django.conf import settings

class EntidadForm(ModelForm):
    class Meta:
        model = Entidad
        fields = '__all__'
        widgets = {
            'tipo': Select(attrs={
                'class': 'form-control',
            }),
            'ruc': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RUC',
            }),
            'razon_social': TextInput(attrs={
                'class': 'form-control',
                'placeholder': u'Razón Social',
            }),
            'direccion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': u'Dirección',
            }),
            'telefono': TextInput(attrs={
                'class': 'form-control',
                'placeholder': u'Teléfono',
            }),
            'celular': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Celular',
            }),
          
        }


class PeriodoCirculacionForm(ModelForm):
    fechainicio_periodo = DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=TextInput(attrs={
            'class': 'form-control datepicker',
        })
    )

    fechafin_periodo = DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=TextInput(attrs={
            'class': 'form-control datepicker',
        })
    )

    class Meta:
        model = PeriodoCirculacion
        exclude = ('razon_social',)
        widgets = {
            'resolucion_autorizacion': TextInput(attrs={
                'class': 'form-control',
            }),
            'nro_cupos': TextInput(attrs={
                'class': 'form-control',
            }),
            'nro_cupos': TextInput(attrs={
                'class': 'form-control',
            }),
            'ruta_autorizada': TextInput(attrs={
                'class': 'form-control',
            }),
            'representante_legal': TextInput(attrs={
                'class': 'form-control',
            }),
            'vehiculo': Select(attrs={
                'class': 'form-control',
            }),
        }

class TarjetaCirculacionForm(ModelForm):
    fecha_expedicion = DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=TextInput(attrs={
            'class': 'form-control datepicker',
        })
    )
    fecha = DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=TextInput(attrs={
            'class': 'form-control datepicker',
        })
    )
    class Meta:
        model = TarjetaCirculacion
        exclude = ('resolucion_autorizacion',)
        widgets = {
            'propietario': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Propietario',
            }),
            'placa': TextInput(attrs={
                'class': 'form-control',
                'placeholder': u'Placa',
            }),
            'clase': Select(attrs={
                'class': 'form-control',
            }),
            'marca': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca',
            }),
            'anio_fabricacion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': u'Año de fabricación',
            }),
            'modelo': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo',
            }),
            'combustible': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Combustible',
            }),
            'nro_ruta': TextInput(attrs={
                'class': 'form-control',
                'placeholder': u'Número de ruta',
            }),
            'color': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Color',
            }),
            'cilindro': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cilindros',
            }),
            'ruedas': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ruedas',
            }),
            'nro_motor': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
            'nro_serie': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
            'pasajeros': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
            'asientos': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
            'peso_seco': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
            'peso_bruto': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
            'frecuencia': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
            'origen': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
            'poliza_seguro': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
          
          
        }