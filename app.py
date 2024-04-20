from flask import Flask, render_template, request
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

def generate_qr_code_from_text(text):
    # Generate QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code to BytesIO object and encode to Base64
    qr_bytes = BytesIO()
    qr_img.save(qr_bytes, format='PNG')
    qr_bytes.seek(0)
    qr_b64 = base64.b64encode(qr_bytes.getvalue()).decode('utf-8')
    
    return qr_b64

@app.route('/', methods=['GET', 'POST'])
def home():
    qr_img = None
    error = None

    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'No file part'
        else:
            file = request.files['file']

            if file.filename == '':
                error = 'No selected file'
            else:
                try:
                    file_content = file.read().decode('utf-8')
                    qr_img = generate_qr_code_from_text(file_content)
                except Exception as e:
                    error = f'Error processing file: {str(e)}'

    return render_template('index.html', qr_img=qr_img, error=error)

if __name__ == '__main__':
    app.run(debug=True)
