from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_pdf_ficha(data, fotos_paths, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    styles = getSampleStyleSheet()
    
    # Fuentes más grandes y limpias
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=14, alignment=1, textColor=colors.HexColor('#1a365d'), spaceAfter=15)
    subtitle_style = ParagraphStyle('SubStyle', fontName='Helvetica-Bold', fontSize=11, alignment=1, spaceAfter=10)
    section_style = ParagraphStyle('SectionStyle', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#1a365d'), spaceBefore=12, spaceAfter=8)
    
    cell_bold = ParagraphStyle('CellBold', fontName='Helvetica-Bold', fontSize=10, leading=12)
    cell_normal = ParagraphStyle('CellNormal', fontName='Helvetica', fontSize=10, leading=12)
    cell_center = ParagraphStyle('CellCenter', fontName='Helvetica', fontSize=10, alignment=1)
    
    story = []

    # ENCABEZADO / MEMBRETE
    story.append(Paragraph("REPÚBLICA BOLIVARIANA DE VENEZUELA<br/>ALCALDÍA DEL MUNICIPIO BOLIVARIANO DE BRIÓN", subtitle_style))
    story.append(Paragraph(data.get('membrete', ''), subtitle_style))
    story.append(Paragraph("RIF: G-20002924-2", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("FICHA TÉCNICA Y REPORTE DE AVANCE DE OBRA", title_style))

    # I. DATOS GENERALES
    story.append(Paragraph("I. DATOS GENERALES", section_style))
    
    ubicacion_completa = f"{data.get('ubicacion', '')} (Parroquia {data.get('parroquia', '')})"
    
    datos_tabla = [
        [Paragraph("<b>Proyecto:</b>", cell_bold), Paragraph(data.get('proyecto', ''), cell_normal), Paragraph("<b>Fecha de Emisión:</b>", cell_bold), Paragraph(data.get('fecha_reporte', ''), cell_normal)],
        [Paragraph("<b>Ubicación:</b>", cell_bold), Paragraph(ubicacion_completa, cell_normal), Paragraph("<b>Período Evaluado:</b>", cell_bold), Paragraph(data.get('periodo_reporte', ''), cell_normal)],
        [Paragraph("<b>Ente Ejecutor:</b>", cell_bold), Paragraph(data.get('ente_ejecutor', ''), cell_normal), Paragraph("<b>Ente Inspector:</b>", cell_bold), Paragraph(data.get('ente_inspector', ''), cell_normal)],
        [Paragraph("<b>Propietario:</b>", cell_bold), Paragraph(data.get('propietario', ''), cell_normal), Paragraph("<b>Cédula:</b>", cell_bold), Paragraph(data.get('cedula', ''), cell_normal)],
        [Paragraph("<b>Datos del Inmueble:</b>", cell_bold), Paragraph(data.get('datos_inmueble', ''), cell_normal), Paragraph("<b>Teléfono:</b>", cell_bold), Paragraph(data.get('telefono', ''), cell_normal)],
        [Paragraph("<b>Tipología:</b>", cell_bold), Paragraph(data.get('tipologia', ''), cell_normal), Paragraph("<b>Tecnología Const.:</b>", cell_bold), Paragraph(data.get('tecnologia', ''), cell_normal)]
    ]

    t_datos = Table(datos_tabla, colWidths=[110, 170, 110, 160])
    t_datos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_datos)
    story.append(Spacer(1, 10))

    # II. TABLA DE AVANCE FÍSICO
    story.append(Paragraph("II. EVALUACIÓN Y TABLA DE AVANCE FÍSICO", section_style))
    fases_tabla = [[Paragraph("<b>Capítulo / Fase Constructiva</b>", cell_bold), Paragraph("<b>Peso (%)</b>", cell_bold), Paragraph("<b>Avance Real (%)</b>", cell_bold), Paragraph("<b>Ponderado (%)</b>", cell_bold)]]
    
    for f in data.get('fases', []):
        fases_tabla.append([
            Paragraph(f['nombre'], cell_normal),
            Paragraph(f"{f['peso']}%", cell_center),
            Paragraph(f"{f['avance_real']:.2f}%", cell_center),
            Paragraph(f"<b>{f['ponderado']:.2f}%</b>", cell_center)
        ])
    
    # Fila de total
    fases_tabla.append([
        Paragraph("<b>PORCENTAJE TOTAL ACUMULADO DE LA OBRA:</b>", ParagraphStyle('Tot', fontName='Helvetica-Bold', fontSize=10, alignment=2)),
        "", "", Paragraph(f"<b>{data.get('total_acumulado', 0):.2f}%</b>", cell_center)
    ])
        
    t_fases = Table(fases_tabla, colWidths=[270, 80, 100, 100])
    t_fases.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2e8f0')), # Fondo fila total
        ('SPAN', (0,-1), (2,-1)), # Combinar celdas para el Total
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_fases)
    story.append(Spacer(1, 10))

    # III. OBSERVACIONES
    story.append(Paragraph("III. OBSERVACIONES GENERALES", section_style))
    obs_tabla = [[Paragraph(data.get('observaciones', 'Sin observaciones.'), cell_normal)]]
    t_obs = Table(obs_tabla, colWidths=[550])
    t_obs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_obs)

    # IV. REGISTRO FOTOGRÁFICO (Agrupado con KeepTogether para evitar superposición)
    if fotos_paths:
        foto_section = [] # Creamos una lista temporal solo para las fotos
        foto_section.append(Spacer(1, 15))
        foto_section.append(Paragraph("IV. REGISTRO FOTOGRÁFICO DE CAMPO", section_style))
        foto_section.append(Spacer(1, 10)) # Espacio extra crucial para evitar choque visual
        
        img_elements = []
        for path in fotos_paths[:4]:
            try:
                img = Image(path, width=260, height=170)
                img_elements.append(img)
            except Exception:
                pass
        
        if img_elements:
            grid_data = []
            if len(img_elements) >= 2:
                grid_data.append([img_elements[0], img_elements[1]])
            else:
                grid_data.append([img_elements[0], ""])
                
            if len(img_elements) == 3:
                grid_data.append([img_elements[2], ""])
            elif len(img_elements) >= 4:
                grid_data.append([img_elements[2], img_elements[3]])

            t_fotos = Table(grid_data, colWidths=[275, 275])
            t_fotos.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ]))
            foto_section.append(t_fotos)
            
        # Añadimos el bloque completo al PDF. Si no cabe, salta entero a la siguiente página.
        story.append(KeepTogether(foto_section))

    doc.build(story)
