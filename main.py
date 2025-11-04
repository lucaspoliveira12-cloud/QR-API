from flask import Flask, Response
import qrcode
import io
import random
import string
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>Servidor de QR Codes ativo ✅</h2>"

@app.route('/qr')
def generate_qr():
    try:
        # Gera um código único
        unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        url = f"https://www.serranegrablog.com/?id={unique_id}"

        # Cria o QR Code em memória
        img = qrcode.make(url)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Retorna a imagem
        return Response(buffer.getvalue(), mimetype='image/png')

    except Exception as e:
        return f"Erro ao gerar QR: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


