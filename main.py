from flask import Flask, Response, redirect, request
import qrcode
import io
import random
import string
import os
import time

app = Flask(__name__)

# Guarda o último QR gerado e o tempo
current_qr = None
qr_created_at = None
EXPIRATION_TIME = 60  # 1 minuto

@app.route('/')
def home():
    return "<h2>Servidor de QR Codes ativo ✅</h2><p>Use /qr para gerar um novo código.</p>"

@app.route('/qr')
def generate_qr():
    global current_qr, qr_created_at
    try:
        # Gera um código único e registra o tempo
        unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        current_qr = unique_id
        qr_created_at = time.time()

        # O QR code leva diretamente para o site principal
        qr_url = f"https://www.serranegrablog.com/erro?id={unique_id}"

        # Cria o QR code com esse link
        img = qrcode.make(qr_url)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return Response(buffer.getvalue(), mimetype='image/png')

    except Exception as e:
        return f"Erro ao gerar QR: {e}"

@app.route('/check')
def check_validity():
    """Endpoint que o site pode consultar para saber se o QR ainda é válido."""
    global current_qr, qr_created_at
    codigo = request.args.get("id")

    # Nenhum QR gerado ainda
    if not current_qr or not qr_created_at:
        return Response("❌ Nenhum QR ativo no momento.", status=403)

    # Se expirou
    if time.time() - qr_created_at > EXPIRATION_TIME:
        return Response("⏰ Expirado", status=403)

    # Se é o atual
    if codigo == current_qr:
        return Response("✅ Válido", status=200)
    else:
        return Response("❌ Inválido", status=403)


@app.route('/invalido')
def invalido():
    """Página ou imagem de QR inválido"""
    return "<h3 style='color:red; text-align:center;'>❌ QR Code inválido ou expirado</h3>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


