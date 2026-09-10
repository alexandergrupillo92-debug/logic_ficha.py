import os
from fpdf import FPDF

# PESOS PONDERADOS OFICIALES (100% TOTAL)
CAPITULOS = [
    ("1. Obras preliminares y preparación", 0.05),
    ("2. Infraestructura y Cimentaciones", 0.15),
    ("3. Superestructura (Columnas y Vigas)", 0.15),
    ("4. Paredes de bloques y marcos", 0.15),
    ("5. Instalaciones sanitarias y eléctricas", 0.10),
    ("6. Cubiertas y techos", 0.10),
    ("7. Revestimientos (frizos y cerámicas)", 0.15),
    ("8. Acabados finales y limpieza", 0.10)
]

class FichaObraPDF(FPDF):
    def __init__(self, direccion_nombre):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.direccion_nombre = str(direccion_nombre).upper()

    def header(self):
        fondo_path = os.path.join('assets', 'membrete_fondo.jpg')
        if os.path.exists(fondo_path):
            self.image(fondo_path, x=0, y=0, w=210, h=297)

        self.set_xy(12, 38)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(20, 60, 120)
        self.cell(186, 5, f"{self.direccion_nombre} · RIF G-20002924-2", ln=True, align='L')
        self.ln(2)

    def footer(self):
        self.set_y(-18)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, f'Página {self.page_no()}', align='C')

def generar_pdf_ficha(datos_form, fotos_paths, output_path):
    pdf = FichaObraPDF(direccion_nombre=datos_form.get('direccion', 'DIRECCIÓN DE HÁBITAT Y VIVIENDA'))
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.add_page()
    
    # TÍTULO PRINCIPAL
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, 'FICHA TÉCNICA Y REPORTE DE AVANCE DE OBRA', ln=True, align='C')
    pdf.ln(2)

    # I. DATOS GENERALES
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(230, 235, 245)
    pdf.cell(0, 5, 'I. DATOS GENERALES', ln=True, fill=True)
    pdf.ln(1)

    campos_i = [
        ("VIVIENDA / DIRECCIÓN:", datos_form.get('direccion_vivienda', '')),
        ("PROPIETARIO:", datos_form.get('propietario', '')),
        ("CÉDULA DE IDENTIDAD:", datos_form.get('cedula', '')),
        ("TELÉFONO:", datos_form.get('telefono', '')),
        ("PARROQUIA:", datos_form.get('parroquia', '')),
        ("TIPOLOGÍA:", datos_form.get('tipologia', '')),
        ("TECNOLOGÍA CONSTRUCTIVA:", datos_form.get('tecnologia', '')),
        ("FECHA:", datos_form.get('fecha', '')),
        ("UBICACIÓN GPS:", f"Ver ubicación satelital ({datos_form.get('gps', 'N/A')})")
    ]

    for label, val in campos_i:
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(48, 4.5, label, border=0)
        pdf.set_font('Helvetica', '', 8)
        pdf.cell(138, 4.5, str(val), border=0, ln=True)

    pdf.ln(2)

    # II. TABLA DE AVANCE FÍSICO PONDERADO
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 5, 'II. EVALUACIÓN Y TABLA DE AVANCE FÍSICO', ln=True, fill=True)
    pdf.ln(1)

    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_fill_color(210, 220, 235)
    pdf.cell(95, 5, 'Capítulo / Fase Constructiva', border=1, align='L', fill=True)
    pdf.cell(25, 5, 'Peso (%)', border=1, align='C', fill=True)
    pdf.cell(30, 5, 'Avance Real (%)', border=1, align='C', fill=True)
    pdf.cell(36, 5, 'Ponderado (%)', border=1, align='C', fill=True)
    pdf.ln()

    pdf.set_font('Helvetica', '', 8)
    total_ponderado = 0.0
    avances_user = datos_form.get('avances', [])

    for i, (cap_nombre, peso) in enumerate(CAPITULOS):
        try:
            av_val = float(avances_user[i]) if i < len(avances_user) else 0.0
        except (ValueError, TypeError):
            av_val = 0.0
        
        av_val = min(max(av_val, 0.0), 100.0)
        pond = (av_val * peso)
        total_ponderado += pond

        pdf.cell(95, 4.8, cap_nombre, border=1, align='L')
        pdf.cell(25, 4.8, f"{int(peso*100)}%", border=1, align='C')
        pdf.cell(30, 4.8, f"{av_val:.1f}%", border=1, align='C')
        pdf.cell(36, 4.8, f"{pond:.2f}%", border=1, align='C')
        pdf.ln()

    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(150, 5.5, 'PORCENTAJE TOTAL ACUMULADO DE LA OBRA:', border=1, align='R', fill=True)
    pdf.cell(36, 5.5, f"{total_ponderado:.2f}%", border=1, align='C', fill=True)
    pdf.ln(7)

    # III. OBSERVACIONES GENERALES
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 5, 'III. OBSERVACIONES GENERALES', ln=True, fill=True)
    pdf.ln(1)
    pdf.set_font('Helvetica', '', 8)
    obs_text = datos_form.get('observaciones', 'Sin observaciones adicionales.')
    pdf.multi_cell(0, 4, str(obs_text), border=0)
    pdf.ln(4)

    # IV. REGISTRO FOTOGRÁFICO
    if fotos_paths:
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(0, 5, 'IV. REGISTRO FOTOGRÁFICO DE CAMPO', ln=True, fill=True)
        pdf.ln(4)

        x_positions = [15, 110, 15, 110]
        y_positions = [48, 48, 140, 140]

        for idx, foto_path in enumerate(fotos_paths[:4]):
            if os.path.exists(foto_path):
                x = x_positions[idx]
                y = y_positions[idx]
                pdf.image(foto_path, x=x, y=y, w=85, h=70)
                pdf.set_xy(x, y + 71)
                pdf.set_font('Helvetica', 'I', 7.5)
                leyenda = datos_form.get(f'desc_foto_{idx+1}', f'Foto N° {idx+1}')
                pdf.cell(85, 4, str(leyenda), align='C')

    pdf.output(output_path)
    
