# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import partial
from io import BytesIO

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, PageBreak
from reportlab.platypus import PageTemplate, BaseDocTemplate, NextPageTemplate, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm, cm, inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39, code93, qr

from base.models import TarjetaCirculacion

def normal_custom(size, alignment):
    return ParagraphStyle(
        name = 'normal_custom_%s' % str(size),
        fontName = 'Helvetica',
        fontSize = size,
        alignment = alignment,
        leading= 9.5
    )

def normal_custom2(size, alignment):
    return ParagraphStyle(
        name = 'normal_custom_%s' % str(size),
        fontName = 'Helvetica',
        fontSize = size,
        alignment = alignment,
    )


def negrita_custom(size, alignment):
    return ParagraphStyle(
        name = 'negrita_custom_%s' % str(size),
        fontName = 'Helvetica-Bold',
        fontSize = size,
        alignment = alignment
    )

@login_required
def tarjeta_print(request, id):
    response = HttpResponse(content_type='application/pdf')
    
    buffer = BytesIO()
    try:
        tarjeta = get_object_or_404(TarjetaCirculacion, pk = id)
    except:
        raise Http404

    report = ImpresionTarjeta(buffer, tarjeta)
    pdf = report.print_tarjeta()
 

    response.write(pdf)

    return response

class ImpresionTarjeta:
    def __init__(self, buffer, tarjeta):
        self.buffer = buffer
        self.tarjeta = tarjeta
        self.pagesize = (8.4 * cm, 5.3 * cm)
        self.width, self.height = self.pagesize

    def primera_hoja_layout(self, canvas, doc):
        canvas.saveState()
        canvas.setPageSize(self.pagesize)
        
        logo = 'static/pag1.jpg'
        canvas.drawImage(logo, 0 * cm, 0 * cm, width = (8.5 * cm), height = (5.28 * cm))

        categoria = Paragraph(u'Vigencia', negrita_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 52 * mm, 32.9 * mm)

        categoria = Paragraph(self.tarjeta.fecha_expedicion.strftime('%d/%m/%Y'), normal_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 42 * mm, 29.5 * mm)

        categoria = Paragraph(self.tarjeta.fecha.strftime('%d/%m/%Y'), normal_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 60 * mm, 29.5 * mm)

        canvas.restoreState()

    def segunda_hoja_layout(self, canvas, doc):
        canvas.saveState()
        canvas.setPageSize(self.pagesize)
        
        logo = 'static/pag2.jpg'
        canvas.drawImage(logo, 0 * cm, 0 * cm, width = (8.5 * cm), height = (5.28 * cm))

        asientos = Paragraph(u'Asientos: <strong>'+str(self.tarjeta.asientos)+'</strong>', normal_custom(8.5, TA_LEFT))
        w, h = asientos.wrap(doc.width, doc.topMargin)
        asientos.drawOn(canvas, 52 * mm, 44.1 * mm)

        cilindros = Paragraph(u'Cilindros: <strong>'+self.tarjeta.cilindro+'</strong>', normal_custom(8.5, TA_LEFT))
        w, h = cilindros.wrap(doc.width, doc.topMargin)
        cilindros.drawOn(canvas, 52 * mm, 40.9 * mm)

        ruedas = Paragraph(u'Ruedas: <strong>'+str(self.tarjeta.ruedas)+'</strong>', normal_custom(8.5, TA_LEFT))
        w, h = ruedas.wrap(doc.width, doc.topMargin)
        ruedas.drawOn(canvas, 52 * mm, 37.8 * mm)

        pesoneto = Paragraph(u'Peso Neto kg: <strong>'+str(self.tarjeta.peso_seco)+'</strong>', normal_custom(8.5, TA_LEFT))
        w, h = pesoneto.wrap(doc.width, doc.topMargin)
        pesoneto.drawOn(canvas, 52 * mm, 34.7 * mm)

        pesobruto = Paragraph(u'Peso Bruto kg: <strong>'+str(self.tarjeta.peso_bruto)+'</strong>', normal_custom(8.5, TA_LEFT))
        w, h = pesobruto.wrap(doc.width, doc.topMargin)
        pesobruto.drawOn(canvas, 52 * mm, 31.2 * mm)

        canvas.restoreState()


    def print_tarjeta(self):
        buffer = self.buffer
        #topMargin = 13 * mm,leftMargin = 23 * mm,rightMargin = 3 * mm,bottomMargin = 1 * mm,showBoundary = 1
        pHeight, pWidth = self.pagesize
        frame1 = Frame(3 * mm, -18 * mm, pHeight, pWidth, id='frame1')
        frame2 = Frame(3 * mm, -3 * mm, pHeight, pWidth, id='frame2')

        primera_hoja = PageTemplate(id='primera_hoja',
                                            frames=[frame1],
                                            onPage=self.primera_hoja_layout)

        segunda_hoja = PageTemplate(id='segunda_hoja',
                                     frames=[frame2],
                                     onPage=self.segunda_hoja_layout)

        elements = []

        p = Paragraph('Placa: <strong>' + self.tarjeta.placa +'</strong>', normal_custom2(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Razon Social: <strong>' + self.tarjeta.resolucion_autorizacion.razon_social.razon_social +'</strong>', normal_custom2(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Propietario: <strong>' + self.tarjeta.propietario + '</strong>' , normal_custom2(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Fecha de Expedicion: <strong>' + str(self.tarjeta.fecha_expedicion) + '</strong>', normal_custom2(8.5, TA_LEFT))
        elements.append(p)


        elements.append(NextPageTemplate('segunda_hoja'))
        elements.append(PageBreak())
        

        p = Paragraph('Clase: <strong>'+ self.tarjeta.clase +'</strong>' , normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Marca: <strong>'+ self.tarjeta.marca +'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Modelo: <strong>'+ self.tarjeta.modelo +'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Año Fabricacion: <strong>'+ str(self.tarjeta.anio_fabricacion)+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Color: <strong>'+ self.tarjeta.color+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Pasajeros: <strong>'+ str(self.tarjeta.pasajeros)+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Motor Nro: <strong>'+self.tarjeta.nro_motor+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Serie Nro: <strong>'+self.tarjeta.nro_serie+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Ruta: <strong>'+str(self.tarjeta.nro_ruta)+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Origen: <strong>'+ self.tarjeta.origen+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Poliza de Seguros: <strong>'+self.tarjeta.poliza_seguro+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Numero de Resolucion: <strong>'+str(self.tarjeta.resolucion_autorizacion)+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        #p = Paragraph(self.tarjeta.resolucion_autorizacion, normal_custom(8.5, TA_LEFT))
        #elements.append(p)

        doc = BaseDocTemplate(buffer,
                              pagesize = self.pagesize)


        doc.addPageTemplates([primera_hoja, segunda_hoja])

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        return pdf
