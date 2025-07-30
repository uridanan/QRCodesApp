from flask import Flask, render_template, request, send_from_directory
import os
from base64 import b64encode
from werkzeug.utils import secure_filename
from jsoninputfile import read_json_from_file, get_json_value 
from qrcodes import generate_qr_code_file, generate_qr_code_bytes


app = Flask(__name__)
UPLOAD_FOLDER = 'tmp/uploads'  # Directory to store uploaded logos
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the directory if it doesn't exist
print(f"Current working directory: {os.getcwd()}")
print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")


@app.route('/tmp/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    qr_code_data_url = None
    logo_url = None
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        url = request.form.get("url")
        if not url:  # URL is mandatory
            return render_template("index.html", error="URL is required")

        logo = request.files.get("logo")
        bg_color = request.form.get("bg_color") or "white"
        fill_color = request.form.get("fill_color") or "black"
        qr_size = int(request.form.get("qr_size")) or 15
        border_size = int(request.form.get("border_size")) or 1

        if border_size > qr_size * 0.1:
            return render_template("index.html", error="Border size cannot exceed 10% of QR size")

        logo_path = None
        if logo and logo.filename:
            logo_filename = secure_filename(logo.filename)
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
            logo.save(logo_path)
            logo_url = logo_filename
        else:
            logo_url = request.form.get("logo_url")
            if logo_url:
                logo_url = secure_filename(logo_url)
                logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_url)
        
        if not logo_url:
                logo_path = os.path.join('static', 'upload image.png')

        try:
            qr_code_image_bytes = generate_qr_code_bytes(url, logo_path, bg_color, fill_color, qr_size, border_size)

            if qr_code_image_bytes:

                qr_code_data_url = "data:image/png;base64," + b64encode(qr_code_image_bytes).decode("utf-8")

                return render_template("index.html", form_data=request.form, logo_url=logo_url, qr_code_data_url=qr_code_data_url)
            else:
                return render_template("index.html", form_data=request.form, logo_url=logo_url, error="QR code generation failed")

        except Exception as e:
            return render_template("index.html", form_data=request.form, logo_url=logo_url, error=f"An error occurred: {e}")

    logo_path = os.path.join('static', 'upload image.png')
    return render_template(
        'index.html',
        form_data={},
        logo_url=None,  # Default logo URL
        qr_code_data_url=None,
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) # Use PORT env var, or fallback to 8000
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    if debug:
        app.debug = True
    else:
        app.debug = False
    app.run(host='0.0.0.0', port=port)