import os
from fpdf import FPDF

class FichaPDF(FPDF):
    def header(self):
        # Fondo membrete oficial si existe en assets
        background_path = os.path.join("assets", "membrete_fondo.jpg")
        if os.path.exists(background_path):
            self.image(background_path, x=0, y=0, w=210, h=297)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def generar_pdf_ficha(data, fotos, output_path="ficha_obra.pdf"):
    pdf = FichaPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Margen superior para no chocar con el membrete
    pdf.set_y(35)
    
    # Título Principal
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(20, 50, 100)
    pdf.cell(0, 8, "FICHA TÉCNICA Y REPORTE DE AVANCE DE OBRA", ln=True, align="C")
    pdf.ln(3)

    # I. DATOS GENERALES Y DEL PROYECTO
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(230, 235, 245)
    pdf.cell(0, 7, " I. DATOS GENERALES Y DEL PROYECTO", ln=True, fill=True)
    pdf.ln(2)

    fields_general = [
        ("Nombre del Proyecto:", data.get('proyecto', '')),
        ("Ente Ejecutor:", data.get('ente_ejecutor', '')),
        ("Ente Inspector:", data.get('ente_inspector', '')),
        ("Propietario / Beneficiario:", data.get('propietario', '')),
        ("Cédula de Identidad:", data.get('cedula', '')),
        ("Teléfono de Contacto:", data.get('telefono', '')),
        ("Parroquia:", data.get('parroquia', '')),
        ("Dirección de la Obra:", data.get('direccion', '')),
        ("N° de Vivienda / Inmueble:", data.get('vivienda_num', '')),
        ("Fecha de Emisión del Reporte:", data.get('fecha_reporte', '')),
        ("Periodo Evaluado:", data.get('periodo_reporte', ''))
    ]

    for label, val in fields_general:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(58, 6, f"  {label}", border=0)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, str(val), border=0)

    pdf.ln(2)

    # II. PERSONAL EN OBRA
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, " II. PERSONAL EN OBRA", ln=True, fill=True)
    pdf.ln(2)

    maestro = data.get('maestro_obra', '0')
    albanil = data.get('albanil', '0')
    obreros = data.get('obreros', '0')
    
    try:
        total_p = int(maestro) + int(albanil) + int(obreros)
    except ValueError:
        total_p = "N/A"

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(45, 6, "  Maestro de Obra:", border=0)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(15, 6, str(maestro), border=0)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(25, 6, "Albañiles:", border=0)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(15, 6, str(albanil), border=0)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(25, 6, "Obreros:", border=0)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(15, 6, str(obreros), border=0)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(30, 6, "Total Personal:", border=0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, str(total_p), border=0, ln=True)

    pdf.ln(3)

    # III. TABLA DE AVANCE FÍSICO POR CAPÍTULO
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, " III. EVALUACIÓN Y TABLA DE AVANCE FÍSICO", ln=True, fill=True)
    pdf.ln(2)

    # Encabezados de tabla
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(110, 6, "Fase Constructiva / Capítulo", border=1, align="C")
    pdf.cell(35, 6, "Avance Real (%)", border=1, align="C")
    pdf.cell(45, 6, "Estatus / Observación", border=1, align="C", ln=True)

    pdf.set_font("Helvetica", "", 9)
    fases = data.get('fases', [])
    for f in fases:
        pdf.cell(110, 6, f"  {f.get('nombre', '')}", border=1)
        pdf.cell(35, 6, f"{f.get('avance', 0)}%", border=1, align="C")
        pdf.cell(45, 6, f.get('estatus', 'Sin iniciar'), border=1, align="C", ln=True)

    # Avance total acumulado
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(110, 7, "  PORCENTAJE TOTAL ACUMULADO DE LA OBRA", border=1)
    pdf.cell(80, 7, f"{data.get('avance_total', 0)}%", border=1, align="C", ln=True)

    pdf.ln(3)

    # IV. OBSERVACIONES / RESUMEN DE ACTIVIDADES
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, " IV. OBSERVACIONES GENERALES Y TRABAJOS DE LA SEMANA", ln=True, fill=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, data.get('observaciones', 'Sin observaciones particulares.'), border=1)

    # V. REGISTRO FOTOGRÁFICO DE CAMPO (EN PÁGINA NUEVA)
    if fotos:
        pdf.add_page()
        pdf.set_y(35)
        
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_fill_color(230, 235, 245)
        pdf.cell(0, 8, " V. REGISTRO FOTOGRÁFICO DE CAMPO", ln=True, fill=True)
        pdf.ln(5)

        # Cuadrícula 2x2 para las fotos
        x_start = 15
        y_start = pdf.get_y()
        w_img = 85
        h_img = 65
        gap_x = 10
        gap_y = 10

        for idx, foto_path in enumerate(fotos[:4]):
            col = idx % 2
            row = idx // 2
            
            pos_x = x_start + col * (w_img + gap_x)
            pos_y = y_start + row * (h_img + gap_y)
            
            pdf.image(foto_path, x=pos_x, y=pos_y, w=w_img, h=h_img)

    pdf.output(output_path)
    return output_path
