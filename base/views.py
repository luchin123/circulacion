# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from serializers import PeriodoCirculacionSerializer
from rest_framework import viewsets, generics
from base.models import PeriodoCirculacion

from django.shortcuts import render

class PeriodoCirculacionViewSet(viewsets.ModelViewSet):
    queryset = PeriodoCirculacion.objects.all()
    serializer_class = PeriodoCirculacionSerializer

class PeriodoCirculacionFilterViewSet(generics.ListAPIView):
    serializer_class = PeriodoCirculacionSerializer

    def get_queryset(self):
        queryset = PeriodoCirculacion.objects.all()
        term = self.request.query_params.get('term', None)

        if term is not None:
            queryset = queryset.filter(resolucion_autorizacion__istartswith = term)
        return queryset
