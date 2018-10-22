from .models import PeriodoCirculacion, Entidad
from rest_framework import serializers

class EntidadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entidad
        fields = ('id', 'razon_social',)

class PeriodoCirculacionSerializer(serializers.HyperlinkedModelSerializer):
    razon_social = EntidadSerializer()
    class Meta:
        model = PeriodoCirculacion
        fields = ('id', 'resolucion_autorizacion', 'razon_social')

