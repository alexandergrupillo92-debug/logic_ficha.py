import os
import uuid
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from logic_ficha import generar_pdf_ficha

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Identificador único para este envío: evita que las fotos y el PDF
        # de un reporte sobrescriban a los de otro reporte.
        run_id = uuid.uuid4().hex[:8]

        # 1. Recibir campos generales
        data = {
            'membrete': request.form.get('membrete', 'DIRECCIÓN DE HÁBITAT Y VIVIENDA'),
            'proyecto': request.form.get('proyecto', ''),
            'parroquia': request.form.get('parroquia', ''),
            'ubicacion': request.form.get('ubicacion', ''),
            'ente_ejecutor': request.form.get('ente_ejecutor', ''),
            'ente_inspector': request.form.get('ente_inspector', ''),
            'propietario': request.form.get('propietario', ''),
            'cedula': request.form.get('cedula', ''),
            'telefono': request.form.get('telefono', ''),
            'datos_inmueble': request.form.get('datos_inmueble', ''),
            'tipologia': request.form.get('tipologia', ''),
            'tecnologia': request.form.get('tecnologia', ''),
            'fecha_reporte': request.form.get('fecha_reporte', ''),
            'periodo_reporte': request.form.get('periodo_reporte', ''),
            'observaciones': request.form.get('observaciones', 'Sin observaciones.')
        }

        # 2. Procesar las 8 Fases Constructivas (Cálculos Ponderados)
        fases_nombres = [
            "1. Obras preliminares y preparación",
            "2. Infraestructura y Cimentaciones",
            "3. Superestructura (Columnas y Vigas)",
            "4. Paredes de bloques y marcos",
            "5. Instalaciones sanitarias y eléctricas",
            "6. Cubiertas y techos",
            "7. Revestimientos (frizos y cerámicas)",
            "8. Acabados finales y limpieza"
        ]
        pesos = [5, 15, 15, 15, 10, 10, 15, 10]
        fases_calculadas = []
        total_acumulado = 0.0

        for i in range(8):
            avance_real_str = request.form.get(f'avance_{i+1}', '0')
            try:
                avance_real = float(avance_real_str)
            except ValueError:
                avance_real = 0.0

            ponderado = (pesos[i] * avance_real) / 100
            total_acumulado += ponderado

            fases_calculadas.append({
                'nombre': fases_nombres[i],
                'peso': pesos[i],
                'avance_real': avance_real,
                'ponderado': ponderado
            })

        data['fases'] = fases_calculadas
        data['total_acumulado'] = total_acumulado

        # 3. Procesar Fotografías con nombre único por envío y por archivo
        #    (antes: file.filename tal cual -> se sobrescribían entre reportes)
        fotos_paths = []
        uploaded_files = request.files.getlist('fotos')
        print(f"[DEBUG] archivos recibidos en 'fotos': {[f.filename for f in uploaded_files]}")

        for idx, file in enumerate(uploaded_files):
            if file and file.filename != '':
                nombre_seguro = secure_filename(file.filename) or f"foto_{idx+1}.jpg"
                nombre_unico = f"{run_id}_{idx+1}_{nombre_seguro}"
                file_path = os.path.join(UPLOAD_FOLDER, nombre_unico)
                file.save(file_path)
                fotos_paths.append(file_path)

        print(f"[DEBUG] fotos_paths guardadas en disco: {fotos_paths}")

        # 4. Generar PDF con nombre único también (evita pisar reportes anteriores)
        nombre_pdf = f"reporte_tecnico_{run_id}.pdf"
        pdf_path = os.path.join(UPLOAD_FOLDER, nombre_pdf)
        generar_pdf_ficha(data, fotos_paths, pdf_path)

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="reporte_tecnico.pdf"  # nombre amigable al descargar
        )

    return render_template('ficha_form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
