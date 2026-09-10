import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


# --- CLASE PARA EL FONDO MEMBRETADO ---
class FondoCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, 'assets', 'membrete_fondo.jpg')
        img_exists = os.path.exists(img_path)

        if not img_exists:
            print(f"[AVISO] No se encontró el membrete en: {img_path}")

        for page in self.pages:
            self.__dict__.update(page)
            if img_exists:
                self.drawImage(
                    img_path, 0, 0,
                    width=letter[0], height=letter[1],
                    preserveAspectRatio=False, mask='auto'
                )
            super().showPage()
        super().save()


# --- FUNCIÓN PRINCIPAL DE GENERACIÓN ---
# Firma alineada con la llamada real en app.py:
#   generar_pdf_ficha(data, fotos_paths, pdf_path)
def generar_pdf_ficha(data, fotos_paths, pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=110,   # no pisar el logo superior del membrete
        bottomMargin=80  # no pisar el pie del membrete
    )
    story = []

    # --- ESTILOS ---
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        'NormalText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11
    )
    label_style = ParagraphStyle(
        'LabelText', parent=normal_style,
        fontName='Helvetica-Bold', fontSize=8.5,
        textColor=colors.HexColor('#1A365D')
    )
    value_style = ParagraphStyle('ValueText', parent=normal_style)
    title_style = ParagraphStyle(
        'TitleText', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=10,
        textColor=colors.HexColor('#1A365D')
    )
    subtitle_style = ParagraphStyle(
        'SubtitleText', parent=normal_style,
        fontName='Helvetica-Bold', alignment=1, fontSize=9,
        textColor=colors.HexColor('#4A5568')
    )

    # --- TÍTULO ---
    story.append(Paragraph(
        "FICHA TÉCNICA Y REPORTE DE AVANCE DE OBRA",
        ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=11,
                        alignment=1, textColor=colors.HexColor('#1A365D'))
    ))
    if data.get('membrete'):
        story.append(Paragraph(data.get('membrete'), subtitle_style))
    story.append(Spacer(1, 15))

    # --- TABLA I. DATOS GENERALES ---
    story.append(Paragraph("I. DATOS GENERALES", title_style))
    story.append(Spacer(1, 5))

    def fila(label1, val1, label2, val2):
        return [
            Paragraph(label1, label_style), Paragraph(val1 or '', value_style),
            Paragraph(label2, label_style), Paragraph(val2 or '', value_style),
        ]

    datos_tabla = [
        fila("Proyecto:", data.get('proyecto', ''),
             "Fecha de Emisión:", data.get('fecha_reporte', '')),
        fila("Parroquia:", data.get('parroquia', ''),
             "Período Evaluado:", data.get('periodo_reporte', '')),
        fila("Ubicación:", data.get('ubicacion', ''),
             "Ente Inspector:", data.get('ente_inspector', '')),
        fila("Ente Ejecutor:", data.get('ente_ejecutor', ''),
             "Propietario:", data.get('propietario', '')),
        fila("Cédula:", data.get('cedula', ''),
             "Teléfono:", data.get('telefono', '')),
        fila("Datos del Inmueble:", data.get('datos_inmueble', ''),
             "Tipología:", data.get('tipologia', '')),
        fila("Tecnología Const.:", data.get('tecnologia', ''), "", ""),
    ]

    t1 = Table(datos_tabla, colWidths=[95, 170, 95, 170])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('BACKGROUND', (3, 0), (3, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#1A365D')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t1)
    story.append(Spacer(1, 15))

    # --- TABLA II. AVANCE FÍSICO ---
    story.append(Paragraph("II. EVALUACIÓN Y TABLA DE AVANCE FÍSICO", title_style))
    story.append(Spacer(1, 5))

    th_style = ParagraphStyle('Th', parent=label_style, textColor=colors.white)
    th_center = ParagraphStyle('ThCenter', parent=th_style, alignment=1)
    center_style = ParagraphStyle('Center', parent=normal_style, alignment=1)

    avance_data = [
        [Paragraph("Capítulo / Fase Constructiva", th_style),
         Paragraph("Peso (%)", th_center),
         Paragraph("Avance Real (%)", th_center),
         Paragraph("Ponderado (%)", th_center)]
    ]

    fases = data.get('fases', [])
    for fase in fases:
        avance_data.append([
            Paragraph(fase.get('nombre', ''), normal_style),
            Paragraph(f"{fase.get('peso', 0)}%", center_style),
            Paragraph(f"{fase.get('avance_real', 0):.2f}%", center_style),
            Paragraph(f"{fase.get('ponderado', 0):.2f}%", center_style),
        ])

    t2 = Table(avance_data, colWidths=[240, 75, 110, 105])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#1A365D')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t2)
    story.append(Spacer(1, 8))

    total = data.get('total_acumulado', 0)
    story.append(Paragraph(
        f"PORCENTAJE TOTAL ACUMULADO DE LA OBRA: {total:.2f}%",
        ParagraphStyle('Total', parent=label_style, fontSize=9)
    ))
    story.append(Spacer(1, 15))

    # --- III. OBSERVACIONES GENERALES ---
    story.append(Paragraph("III. OBSERVACIONES GENERALES", title_style))
    story.append(Spacer(1, 5))
    observaciones = (data.get('observaciones') or '').strip()
    story.append(Paragraph(observaciones or 'Sin observaciones.', normal_style))
    story.append(Spacer(1, 15))

    # --- IV. REGISTRO FOTOGRÁFICO DE CAMPO ---
    story.append(Paragraph("IV. REGISTRO FOTOGRÁFICO DE CAMPO", title_style))
    story.append(Spacer(1, 8))

    print(f"[DEBUG] fotos_paths recibidas: {fotos_paths}")

    if not fotos_paths:
        story.append(Paragraph(
            "No se registraron fotografías para este período.", normal_style
        ))
    else:
        img_w, img_h = 2.4 * inch, 1.8 * inch
        fila_imgs, fila_actual = [], []

        for ruta in fotos_paths:
            try:
                if not os.path.exists(ruta):
                    raise FileNotFoundError(f"no existe en disco: {ruta}")
                celda = Image(ruta, width=img_w, height=img_h)
            except Exception as e:
                print(f"[AVISO] No se pudo cargar la foto {ruta}: {e}")
                celda = Paragraph(
                    f"(imagen no disponible: {os.path.basename(str(ruta))} — {e})",
                    normal_style
                )
            fila_actual.append(celda)
            if len(fila_actual) == 2:
                fila_imgs.append(fila_actual)
                fila_actual = []
        if fila_actual:
            fila_actual.append("")  # completar la fila impar
            fila_imgs.append(fila_actual)

        t3 = Table(fila_imgs, colWidths=[img_w + 10, img_w + 10])
        t3.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(t3)

    doc.build(story, canvasmaker=FondoCanvas)
    return pdf_path
