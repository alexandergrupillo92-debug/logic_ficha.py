import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# 1. CLASE PARA DIBUJAR EL MEMBRETE DE FONDO
class FondoCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for page in self.pages:
            self.__dict__.update(page)
            # Ruta a la imagen del membrete en la carpeta assets
            img_path = os.path.join(os.path.dirname(__file__), 'assets', 'membrete_fondo.jpg')
            if os.path.exists(img_path):
                # Dibuja la imagen ocupando toda la carta (612x792 puntos)
                self.drawImage(img_path, 0, 0, width=letter[0], height=letter[1])
            super().showPage()
        super().save()

# 2. FUNCIÓN PRINCIPAL PARA GENERAR EL PDF
def crear_pdf_ficha(data):
    # Se aumentan los márgenes superior e inferior para no tapar los logos
    doc = SimpleDocTemplate(
        "reporte_tecnico.pdf",
        pagesize=letter,
        rightMargin=40, 
        leftMargin=40,
        topMargin=110,  # Espacio para el logo superior
        bottomMargin=80 # Espacio para el pie de página
    )
    story = []

    # --- ESTILOS DE TEXTO ---
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle('NormalText', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11)
    bold_style = ParagraphStyle('BoldText', parent=normal_style, fontName='Helvetica-Bold')
    title_style = ParagraphStyle('TitleText', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#1A365D'))

    # Título Principal
    story.append(Paragraph("FICHA TÉCNICA Y REPORTE DE AVANCE DE OBRA", ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=11, alignment=1, textColor=colors.HexColor('#1A365D'))))
    story.append(Spacer(1, 15))

    # --- I. DATOS GENERALES ---
    story.append(Paragraph("I. DATOS GENERALES", title_style))
    story.append(Spacer(1, 5))

    datos_tabla = [
        [Paragraph("<b>Proyecto:</b>", normal_style), Paragraph(data.get('proyecto', 'CASAS DE CURIEPE'), normal_style), 
         Paragraph("<b>Fecha de Emisión:</b>", normal_style), Paragraph(data.get('fecha', ''), normal_style)],
        
        [Paragraph("<b>Ubicación:</b>", normal_style), Paragraph(data.get('ubicacion', ''), normal_style), 
         Paragraph("<b>Período Evaluado:</b>", normal_style), Paragraph(data.get('periodo', ''), normal_style)],
        
        [Paragraph("<b>Ente Ejecutor:</b>", normal_style), Paragraph(data.get('ejecutor', 'SECRETARÍA DE VIVIENDA DE LA GOBERNACIÓN DE MIRANDA'), normal_style), 
         Paragraph("<b>Ente Inspector:</b>", normal_style), Paragraph("DIRECCIÓN DE INGENIERÍA MUNICIPAL", normal_style)],
        
        [Paragraph("<b>Propietario:</b>", normal_style), Paragraph(data.get('propietario', ''), normal_style), 
         Paragraph("<b>Cédula:</b>", normal_style), Paragraph(data.get('cedula', ''), normal_style)],
        
        [Paragraph("<b>Datos del Inmueble:</b>", normal_style), Paragraph(data.get('inmueble', ''), normal_style), 
         Paragraph("<b>Teléfono:</b>", normal_style), Paragraph(data.get('telefono', ''), normal_style)],
        
        [Paragraph("<b>Tipología:</b>", normal_style), Paragraph(data.get('tipologia', 'Unifamiliar'), normal_style), 
         Paragraph("<b>Tecnología Const.:</b>", normal_style), Paragraph(data.get('tecnologia', 'Estructura Aporticada'), normal_style)]
    ]

    # Ajuste de anchos de columna para que quede simétrico
    t1 = Table(datos_tabla, colWidths=[95, 170, 95, 170])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t1)
    story.append(Spacer(1, 15))

    # --- II. TABLA DE AVANCE FÍSICO ---
    story.append(Paragraph("II. EVALUACIÓN Y TABLA DE AVANCE FÍSICO", title_style))
    story.append(Spacer(1, 5))

    # Encabezados
    avance_data = [
        [Paragraph("<b>Capítulo / Fase Constructiva</b>", ParagraphStyle('Th', parent=bold_style, textColor=colors.white)),
         Paragraph("<b>Peso (%)</b>", ParagraphStyle('Th', parent=bold_style, textColor=colors.white, alignment=1)),
         Paragraph("<b>Avance Real (%)</b>", ParagraphStyle('Th', parent=bold_style, textColor=colors.white, alignment=1)),
         Paragraph("<b>Ponderado (%)</b>", ParagraphStyle('Th', parent=bold_style, textColor=colors.white, alignment=1))]
    ]
    
    # Filas de ejemplo (reemplaza con tus variables dinámicas)
    avance_data.append([Paragraph("1. Obras preliminares y preparación", normal_style), Paragraph("5%", normal_style), Paragraph("100.00%", normal_style), Paragraph("5.00%", normal_style)])
    avance_data.append([Paragraph("2. Infraestructura y Cimentaciones", normal_style), Paragraph("15%", normal_style), Paragraph("100.00%", normal_style), Paragraph("15.00%", normal_style)])
    # ... agrega las demás filas aquí ...

    t2 = Table(avance_data, colWidths=[240, 75, 110, 105])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')), # Color azul oscuro para el encabezado
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t2)
    
    # 3. CONSTRUCCIÓN DEL DOCUMENTO USANDO EL FONDO
    doc.build(story, canvasmaker=FondoCanvas)
