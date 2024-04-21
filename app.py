from flask import Flask, render_template, request
import qrcode
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

def generate_qr_code_from_text(text):
    # Generate QR code image using qrcode library
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert QR code image to PIL Image
    img_pil = qr_img.get_image()

    # Create BytesIO object to hold image data
    img_bytesio = BytesIO()
    img_pil.save(img_bytesio, format='PNG')  # Save PIL Image to BytesIO as PNG

    # Encode image data as base64 string
    img_b64 = base64.b64encode(img_bytesio.getvalue()).decode('utf-8')

    return img_b64

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
    app.run(host='0.0.0.0', port=5000)
