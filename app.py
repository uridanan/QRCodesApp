from flask import Flask, render_template, request, send_from_directory
import os
from base64 import b64encode
from qr_generator import read_json_from_file, get_json_value, generate_qr_code_file, generate_qr_code_bytes

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'  # Directory to store uploaded logos
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the directory if it doesn't exist
print(f"Current working directory: {os.getcwd()}")
print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")

@app.route("/", methods=["GET", "POST"])
def index():
    qr_code_image = None
    qr_code_data_url = None
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
        if logo:
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo.filename)
            logo.save(logo_path)

        try:
            qr_code_image_bytes = generate_qr_code_bytes(url, logo_path, bg_color, fill_color, qr_size, border_size)

            if qr_code_image_bytes:

                qr_code_data_url = "data:image/png;base64," + b64encode(qr_code_image_bytes).decode("utf-8")

                return render_template("index.html", qr_code_data_url=qr_code_data_url)
            else:
                return render_template("index.html", error="QR code generation failed")

        except Exception as e:
            return render_template("index.html", error=f"An error occurred: {e}")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)