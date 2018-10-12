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
        alignment = alignment
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
        
        logo = 'logo/pag1.jpg'
        canvas.drawImage(logo, 0 * cm, 0 * cm, width = (8.5 * cm), height = (5.28 * cm))

        categoria = Paragraph(u'Vigencia', negrita_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 52 * mm, 16.9 * mm)

        categoria = Paragraph(self.tarjeta.fecha_expedicion.strftime('%d/%m/%Y'), normal_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 53 * mm, 12.5 * mm)

        categoria = Paragraph(self.tarjeta.fecha.strftime('%d/%m/%Y'), normal_custom(8.5, TA_LEFT))
        w, h = categoria.wrap(doc.width, doc.topMargin)
        categoria.drawOn(canvas, 53 * mm, 12.5 * mm)

        canvas.restoreState()

    def segunda_hoja_layout(self, canvas, doc):
        canvas.saveState()
        canvas.setPageSize(self.pagesize)
        
        logo = 'static/pag2.jpg'
        canvas.drawImage(logo, 0 * cm, 0 * cm, width = (8.5 * cm), height = (5.28 * cm))

        asientos = Paragraph(u'Asientos', negrita_custom(8.5, TA_LEFT))
        w, h = asientos.wrap(doc.width, doc.topMargin)
        asientos.drawOn(canvas, 52 * mm, 56.9 * mm)

        asientos = Paragraph(str(self.tarjeta.asientos), normal_custom(8.5, TA_LEFT))
        w, h = asientos.wrap(doc.width, doc.topMargin)
        asientos.drawOn(canvas, 56 * mm, 52.5 * mm)

        cilindros = Paragraph(u'Cilindros', negrita_custom(8.5, TA_LEFT))
        w, h = cilindros.wrap(doc.width, doc.topMargin)
        cilindros.drawOn(canvas, 52 * mm, 46.9 * mm)

        cilindros = Paragraph(self.tarjeta.cilindro, normal_custom(8.5, TA_LEFT))
        w, h = cilindros.wrap(doc.width, doc.topMargin)
        cilindros.drawOn(canvas, 56 * mm, 42.5 * mm)

        ruedas = Paragraph(u'Ruedas', negrita_custom(8.5, TA_LEFT))
        w, h = ruedas.wrap(doc.width, doc.topMargin)
        ruedas.drawOn(canvas, 52 * mm, 36.9 * mm)

        ruedas = Paragraph(str(self.tarjeta.ruedas), normal_custom(8.5, TA_LEFT))
        w, h = ruedas.wrap(doc.width, doc.topMargin)
        ruedas.drawOn(canvas, 56 * mm, 32.5 * mm)

        pesoneto = Paragraph(u'Peso Neto kg:', negrita_custom(8.5, TA_LEFT))
        w, h = pesoneto.wrap(doc.width, doc.topMargin)
        pesoneto.drawOn(canvas, 52 * mm, 26.9 * mm)

        pesoneto = Paragraph(str(self.tarjeta.peso_seco), normal_custom(8.5, TA_LEFT))
        w, h = pesoneto.wrap(doc.width, doc.topMargin)
        pesoneto.drawOn(canvas, 56 * mm, 22.5 * mm)

        pesobruto = Paragraph(u'Peso Bruto kg:', negrita_custom(8.5, TA_LEFT))
        w, h = pesobruto.wrap(doc.width, doc.topMargin)
        pesobruto.drawOn(canvas, 52 * mm, 16.9 * mm)

        pesobruto = Paragraph(str(self.tarjeta.peso_bruto), normal_custom(8.5, TA_LEFT))
        w, h = pesobruto.wrap(doc.width, doc.topMargin)
        pesobruto.drawOn(canvas, 56 * mm, 12.5 * mm)

        canvas.restoreState()


    def print_tarjeta(self):
        buffer = self.buffer
        #topMargin = 13 * mm,leftMargin = 23 * mm,rightMargin = 3 * mm,bottomMargin = 1 * mm,showBoundary = 1
        pHeight, pWidth = self.pagesize
        frame1 = Frame(24 * mm, -13 * mm, pHeight, pWidth, id='frame1')
        frame2 = Frame(4 * mm, -2 * mm, pHeight, pWidth, id='frame2')

        primera_hoja = PageTemplate(id='primera_hoja',
                                            frames=[frame1],
                                            onPage=self.primera_hoja_layout)

        segunda_hoja = PageTemplate(id='segunda_hoja',
                                     frames=[frame2],
                                     onPage=self.segunda_hoja_layout)

        elements = []

        p = Paragraph('Placa', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(self.tarjeta.placa, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Razon Social', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(self.tarjeta.resolucion_autorizacion.razon_social.razon_social, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Propietario', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(str(self.tarjeta.propietario), normal_custom(8.5, TA_LEFT))
        elements.append(p)

        elements.append(NextPageTemplate('segunda_hoja'))
        elements.append(PageBreak())
        

        p = Paragraph('Clase', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(self.tarjeta.clase, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Marca', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(self.tarjeta.marca, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Modelo', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(self.tarjeta.modelo, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(u'Año Fabricacion', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(str(self.tarjeta.anio_fabricacion), normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Color', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(self.tarjeta.color, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Pasajeros', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(str(self.tarjeta.pasajeros), normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Motor Nro', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(self.tarjeta.nro_motor, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Serie Nro', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(self.tarjeta.nro_serie, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Ruta', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(str(self.tarjeta.nro_ruta), normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Origen', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(self.tarjeta.origen, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Poliza de Seguros', negrita_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph(self.tarjeta.poliza_seguro, normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Numero de Resolucion', negrita_custom(8.5, TA_LEFT))
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
