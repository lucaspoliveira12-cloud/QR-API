from flask import Flask, Response, redirect, request
import qrcode
import io
import random
import string
import os
import time

app = Flask(__name__)

# Mantém o último código e o tempo de criação
current_qr = None
qr_created_at = None
EXPIRATION_TIME = 300  # segundos

@app.route('/')
def home():
    return "<h2>Servidor de QR Codes ativo ✅</h2><p>Use /qr para gerar um novo código.</p>"

@app.route('/qr')
def generate_qr():
    global current_qr, qr_created_at
    try:
        # Gera um código único e registra a hora
        unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        current_qr = unique_id
        qr_created_at = time.time()

        # O QR code aponta para o endpoint /redirect do servidor
        qr_url = f"https://qr-api-1-63iq.onrender.com/redirect?id={unique_id}"

        # Cria o QR code com esse link
        img = qrcode.make(qr_url)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return Response(buffer.getvalue(), mimetype='image/png')

    except Exception as e:
        return f"Erro ao gerar QR: {e}"

@app.route('/redirect')
def redirect_qr():
    """Redireciona para a página certa dependendo do tempo"""
    global current_qr, qr_created_at

    codigo = request.args.get("id")

    # Nenhum QR foi gerado ainda
    if not current_qr or not qr_created_at:
        return redirect("https://www.serranegrablog.com/erro")

    # Se passou de 1 minuto → redireciona para página de erro
    if time.time() - qr_created_at > EXPIRATION_TIME:
        return redirect("https://www.serranegrablog.com/erro")

    # Se for o QR atual → redireciona para a landing page
    if codigo == current_qr:
        return redirect(f"https://www.serranegrablog.com/app-landing-page?id={codigo}")
    else:
        return redirect("https://www.serranegrablog.com/erro")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)





