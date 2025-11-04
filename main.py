from flask import Flask, Response, request
import qrcode
import io
import random
import string
import os
import time

app = Flask(__name__)

# Armazena o último código válido e o momento da criação
last_code = None
code_timestamp = None
EXPIRATION_TIME = 60  # segundos (1 minuto)

@app.route('/')
def home():
    return "<h2>Servidor de QR Codes ativo ✅</h2><p>Use /qr para gerar um novo QR code.</p>"

@app.route('/qr')
def generate_qr():
    global last_code, code_timestamp
    try:
        # Gera um código único
        unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        last_code = unique_id
        code_timestamp = time.time()  # marca o horário de criação

        # O link que o QR vai abrir
        url = f"https://qr-api-vl7v.onrender.com/validar?id={unique_id}"  # seu domínio Render

        # Cria o QR Code em memória
        img = qrcode.make(url)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Retorna a imagem
        return Response(buffer.getvalue(), mimetype='image/png')

    except Exception as e:
        return f"Erro ao gerar QR: {e}"

@app.route('/validar')
def validar_qr():
    """Verifica se o QR ainda é válido (não expirou e é o mais recente)"""
    global last_code, code_timestamp
    codigo = request.args.get("id")

    # Se não há código ativo ainda
    if not last_code or not code_timestamp:
        return "<h3 style='color:red;'>❌ Nenhum QR ativo no momento.</h3>", 403

    # Verifica se já passou 1 minuto
    if time.time() - code_timestamp > EXPIRATION_TIME:
        return "<h3 style='color:red;'>⏰ QR Code expirado (tempo esgotado)!</h3>", 403

    # Verifica se é o código atual
    if codigo == last_code:
        return "<h3 style='color:green;'>✅ QR Code válido!</h3>"
    else:
        return "<h3 style='color:red;'>❌ QR Code inválido ou antigo!</h3>", 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



