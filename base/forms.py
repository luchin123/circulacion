# -*- coding: utf-8 -*-

from django.forms import ModelForm, TextInput, Select, Textarea, DateField, CheckboxInput, FileInput

from models import Entidad, Periodo_Circulacion, Tarjeta_Circulacion
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
                'placeholder': 'Razon Social',
            }),
            'direccion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Direccion',
            }),
            'telefono': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefono',
            }),
            'celular': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Celular',
            }),
            'administracion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Administracion',
            }),
          
        }


class Periodo_CirculacionForm(ModelForm):
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
        model = Periodo_Circulacion
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

class Tarjeta_CirculacionForm(ModelForm):
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
        model = Tarjeta_Circulacion
        exclude = ('persona',)
        widgets = {
            'propietario': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres',
            }),
            'placa': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numero Papeleta',
            }),
            'clase': Select(attrs={
                'class': 'form-control',
            }),
            'marca': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entidad',
            }),
            'anio_fabricacion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Comisaria',
            }),
            'modelo': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'infraccion',
            }),
            'combustible': Select(attrs={
                'class': 'form-control',
            }),
            'nro_ruta': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'infraccion',
            }),
            'color': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Grado de Alcohol',
            }),
            'cilindro': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
            }),
            'ruedas': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carnet',
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