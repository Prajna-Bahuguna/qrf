from flask import Flask, render_template, request
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def generate_qr_code():
    if request.method == 'POST':
        text = request.form['text']  # Get text entered by the user
        
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
        
        # Render template with QR code Base64 string
        return render_template('index.html', qr_img=qr_b64)

    # Render default template for GET request
    return render_template('index.html', qr_img=None)

if __name__ == '__main__':
    app.run(debug=True)
