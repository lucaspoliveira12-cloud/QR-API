from flask import Flask, Response, request
import qrcode
import io
import random
import string
import os

app = Flask(__name__)

# Armazena o último código válido
last_code = None

@app.route('/')
def home():
    return "<h2>Servidor de QR Codes ativo ✅</h2><p>Use /qr para gerar um novo QR code.</p>"

@app.route('/qr')
def generate_qr():
    global last_code
    try:
        # Gera um código único
        unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        last_code = unique_id  # Atualiza o último código válido

        # O link que o QR vai abrir (página de verificação)
        url = f"https://qr-api-vl7v.onrender.com/validar?id={unique_id}"  # use o seu domínio do Render

        # Cria o QR Code em memória
        img = qrcode.make(url)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Retorna a imagem PNG
        return Response(buffer.getvalue(), mimetype='image/png')

    except Exception as e:
        return f"Erro ao gerar QR: {e}"

@app.route('/validar')
def validar_qr():
    """Verifica se o QR ainda é o mais recente"""
    global last_code
    codigo = request.args.get("id")

    if codigo == last_code:
        return "<h3 style='color:green;'>✅ QR Code ainda válido!</h3>"
    else:
        return "<h3 style='color:red;'>❌ QR Code expirado!</h3>", 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


