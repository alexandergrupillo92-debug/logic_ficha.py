import os
from flask import Flask, render_template, request, send_file
from logic_ficha import generar_pdf_ficha

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Recibir campos del formulario
        data = {
            'proyecto': request.form.get('proyecto', ''),
            'ente_ejecutor': request.form.get('ente_ejecutor', ''),
            'ente_inspector': request.form.get('ente_inspector', ''),
            'propietario': request.form.get('propietario', ''),
            'cedula': request.form.get('cedula', ''),
            'telefono': request.form.get('telefono', ''),
            'parroquia': request.form.get('parroquia', ''),
            'direccion': request.form.get('direccion', ''),
            'vivienda_num': request.form.get('vivienda_num', ''),
            'fecha_reporte': request.form.get('fecha_reporte', ''),
            'periodo_reporte': request.form.get('periodo_reporte', ''),
            'maestro_obra': request.form.get('maestro_obra', '0'),
            'albanil': request.form.get('albanil', '0'),
            'obreros': request.form.get('obreros', '0'),
            'avance_total': request.form.get('avance_total', '0'),
            'observaciones': request.form.get('observaciones', '')
        }

        # Procesar fases de la obra
        nombres_fases = request.form.getlist('fase_nombre')
        avances_fases = request.form.getlist('fase_avance')
        estatus_fases = request.form.getlist('fase_estatus')

        fases = []
        for n, a, e in zip(nombres_fases, avances_fases, estatus_fases):
            fases.append({'nombre': n, 'avance': a, 'estatus': e})
        data['fases'] = fases

        # Procesar fotos de campo
        fotos_paths = []
        uploaded_files = request.files.getlist('fotos')
        for file in uploaded_files:
            if file and file.filename != '':
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                fotos_paths.append(file_path)

        # Generar PDF
        pdf_path = os.path.join(UPLOAD_FOLDER, "reporte_avance.pdf")
        generar_pdf_ficha(data, fotos_paths, pdf_path)

        return send_file(pdf_path, as_attachment=True)

    return render_template('ficha_form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
