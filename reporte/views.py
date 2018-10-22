# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import partial
from io import BytesIO

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter, A4, landscape

from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, PageBreak, TableStyle
from reportlab.platypus import PageTemplate, BaseDocTemplate, NextPageTemplate, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm, cm, inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39, code93, qr

from base.models import TarjetaCirculacion, Autoridad, Entidad

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

def normal_custom3(size, alignment):
    return ParagraphStyle(
        name = 'normal_custom_%s' % str(size),
        fontName = 'Helvetica-Bold',
        fontSize = 6,
        alignment = alignment,
    )


def negrita_custom(size, alignment):
    return ParagraphStyle(
        name = 'negrita_custom_%s' % str(size),
        fontName = 'Helvetica-Bold',
        fontSize = size,
        alignment = alignment
    )

def table_estilo():
    return TableStyle(
        [
            ('FONTNAME', (0,0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1, -1), 7),
            ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
            ('BOX', (0,0), (-1, -1), 0.25, colors.black),
            ('ALIGNMENT', (0,0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0,0), (-1, -1), 1),
            ('TOPPADDING', (0,0), (-1, -1), 1),
        ]
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

@login_required
def vehiculos_pdf(request, id):
    response = HttpResponse(content_type='application/pdf')
    
    buffer = BytesIO()

    try:
        empresa = get_object_or_404(Entidad, pk = id)
    except:
        raise Http404

    report = ImpresionVehiculos(buffer, 'A4')
    pdf = report.print_vehiculos(empresa)
 

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

        vehiculo = Paragraph( self.tarjeta.resolucion_autorizacion.get_vehiculo_display().upper()  , normal_custom3(8.5, TA_LEFT))
        w, h = vehiculo.wrap(doc.width, doc.topMargin)
        vehiculo.drawOn(canvas, 60 * mm, 38.05 * mm)

        canvas.restoreState()

    def segunda_hoja_layout(self, canvas, doc):
        canvas.saveState()
        canvas.setPageSize(self.pagesize)
        
        logo = 'static/pag2.jpg'
        canvas.drawImage(logo, 0 * cm, 0 * cm, width = (8.5 * cm), height = (5.28 * cm))

        autoridad = Autoridad.objects.filter(activo = True)
        if autoridad.count() > 0:
            autoridad = autoridad[0]

            firma = str(autoridad.firma_autoridad)
            canvas.drawImage(firma, 54.3 * mm, 2 * cm, width = (2.6 * cm), height = (1 * cm))

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

        p = Paragraph('Razón Social: <strong>' + self.tarjeta.resolucion_autorizacion.razon_social.razon_social +'</strong>', normal_custom2(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Propietario: <strong>' + self.tarjeta.propietario + '</strong>' , normal_custom2(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Fecha de Expedición: <strong>' + str(self.tarjeta.fecha_expedicion) + '</strong>', normal_custom2(8.5, TA_LEFT))
        elements.append(p)


        elements.append(NextPageTemplate('segunda_hoja'))
        elements.append(PageBreak())
        

        p = Paragraph('Clase: <strong>'+ self.tarjeta.clase +'</strong>' , normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Marca: <strong>'+ self.tarjeta.marca +'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Modelo: <strong>'+ self.tarjeta.modelo +'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Año Fabricación: <strong>'+ str(self.tarjeta.anio_fabricacion)+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Color: <strong>'+ self.tarjeta.color+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Pasajeros: <strong>'+ str(self.tarjeta.pasajeros)+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Motor Nro: <strong>'+self.tarjeta.nro_motor+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Serie Nro: <strong>'+self.tarjeta.nro_serie+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Número de Ruta: <strong>'+str(self.tarjeta.nro_ruta)+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Origen: <strong>'+ self.tarjeta.origen+'</strong>', normal_custom(8.5, TA_LEFT))
        elements.append(p)

        p = Paragraph('Número de Resolución: <strong>'+str(self.tarjeta.resolucion_autorizacion)+'</strong>', normal_custom(8.5, TA_LEFT))
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

class ImpresionVehiculos:
  def __init__(self, buffer, pagesize):
    self.buffer = buffer
    if pagesize == 'A4':
      self.pagesize = landscape(A4)
    elif pagesize == 'Letter':
      self.pagesize = letter
      self.width, self.height = self.pagesize

  @staticmethod
  def _header_footer(canvas, doc, empresa):
    canvas.saveState()

    ##logo = 'front/static/front/images/peru.jpg'

    #canvas.drawImage(logo, doc.leftMargin + 50, doc.height + doc.topMargin + 160, width = (2.3 * cm), height = (2.3 * cm))
    

    # Cabecera
    header = Paragraph('Municipalidad Provincial de Urubamba', negrita_custom(9, TA_CENTER))
    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin)

    header = Paragraph('Listado de vehiculos por empresa', negrita_custom(10, TA_CENTER))
    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 5 * mm)

    header = Paragraph(empresa.razon_social, negrita_custom(8, TA_CENTER) )
    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 10 * mm)

    canvas.restoreState()


  def print_vehiculos(self, empresa):
    buffer = self.buffer
    doc = SimpleDocTemplate(buffer, pagesize = self.pagesize, topMargin = 60, leftMargin = 50, rightMargin = 50, bottomMargin = 20, showBoundary = 0)

    elements  = []



    detalles_data = [
        ['Propietario', 'Placa', 'Clase', 'Marca', 'Año Fabricacion', 'Modelo', 'Ruta', 'Pasajeros', 'Poliza'],
    ]

    tarjetas = TarjetaCirculacion.objects.filter(resolucion_autorizacion__razon_social__id = empresa.id)

    for tarjeta in tarjetas:
        propietario = Paragraph(tarjeta.propietario, normal_custom(7, TA_LEFT))
        placa = Paragraph(tarjeta.placa, normal_custom(7, TA_LEFT))
        clase = Paragraph(tarjeta.clase, normal_custom(7, TA_LEFT))
        marca = Paragraph(tarjeta.marca, normal_custom(7, TA_LEFT))
        anio_fabricacion = Paragraph(str(tarjeta.anio_fabricacion), normal_custom(7, TA_LEFT))
        modelo = Paragraph(tarjeta.modelo, normal_custom(7, TA_LEFT))
        nro_ruta = Paragraph(str(tarjeta.nro_ruta), normal_custom(7, TA_LEFT))
        pasajeros = Paragraph(str(tarjeta.pasajeros), normal_custom(7, TA_LEFT))
        poliza = Paragraph(tarjeta.poliza_seguro, normal_custom(7, TA_LEFT))
        detalles_data.append([
          propietario, placa, clase, marca, anio_fabricacion, modelo, nro_ruta, pasajeros, poliza
        ])

    detalles_tabla = Table(detalles_data, colWidths = [None], style = table_estilo(),
    repeatRows = 1)

    elements.append(detalles_tabla)


    doc.build(elements, onFirstPage = partial(self._header_footer, empresa = empresa),
      onLaterPages = partial(self._header_footer, empresa = empresa), canvasmaker = NumberedCanvas)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf

class NumberedCanvas(canvas.Canvas):
  def __init__(self, *args, **kwargs):
    canvas.Canvas.__init__(self, *args, **kwargs)
    self._saved_page_states = []

  def showPage(self):
    self._saved_page_states.append(dict(self.__dict__))
    self._startPage()

  def save(self):
    """add page info to each page (page x of y)"""
    num_pages = len(self._saved_page_states)
    for state in self._saved_page_states:
      self.__dict__.update(state)
      self.draw_page_number(num_pages)
      canvas.Canvas.showPage(self)
      canvas.Canvas.save(self)

  def draw_page_number(self, page_count):
    # Change the position of this to wherever you want the page number to be
    self.setFont('Helvetica', 9)
    self.drawRightString(286 * mm, 205 * mm,
      u"Página %d de %d" % (self._pageNumber, page_count))