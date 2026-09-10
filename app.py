import os
from flask import Flask, render_template, request, send_file
from logic_ficha import generar_pdf_ficha

app = Flask(__name__)

# Carpeta temporal para procesar archivos e imágenes en Render
UPLOAD_FOLDER = '/tmp/uploads' if os.path.exists('/tmp') else 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('ficha_form.html')

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    datos_form = {
        'direccion': request.form.get('direccion'),
        'propietario': request.form.get('propietario'),
        'cedula': request.form.get('cedula'),
        'telefono': request.form.get('telefono'),
        'direccion_vivienda': request.form.get('direccion_vivienda'),
        'parroquia': request.form.get('parroquia'),
        'tipologia': request.form.get('tipologia'),
        'tecnologia': request.form.get('tecnologia'),
        'fecha': request.form.get('fecha'),
        'gps': request.form.get('gps'),
        'observaciones': request.form.get('observaciones'),
        'avances': [
            request.form.get('avance_1', 0),
            request.form.get('avance_2', 0),
            request.form.get('avance_3', 0),
            request.form.get('avance_4', 0),
            request.form.get('avance_5', 0),
            request.form.get('avance_6', 0),
            request.form.get('avance_7', 0),
            request.form.get('avance_8', 0)
        ],
        'desc_foto_1': request.form.get('desc_foto_1', ''),
        'desc_foto_2': request.form.get('desc_foto_2', ''),
        'desc_foto_3': request.form.get('desc_foto_3', ''),
        'desc_foto_4': request.form.get('desc_foto_4', '')
    }

    fotos_paths = []
    for i in range(1, 5):
        foto = request.files.get(f'foto_{i}')
        if foto and foto.filename != '':
            foto_path = os.path.join(UPLOAD_FOLDER, f"temp_{i}_{foto.filename}")
            foto.save(foto_path)
            fotos_paths.append(foto_path)

    output_pdf = os.path.join(UPLOAD_FOLDER, "ficha_tecnica.pdf")
    generar_pdf_ficha(datos_form, fotos_paths, output_pdf)

    return send_file(output_pdf, as_attachment=True, download_name="Ficha_Tecnica_Obra.pdf")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
  
