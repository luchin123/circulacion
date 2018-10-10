from .models import PeriodoCirculacion
from rest_framework import serializers

class PeriodoCirculacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PeriodoCirculacion
        fields = ('id', 'resolucion_autorizacion',)
