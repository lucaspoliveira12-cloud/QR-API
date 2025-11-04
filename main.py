from flask import Flask, Response, request
import qrcode
import io
import random
import string
import os
import time

app = Flask(__name__)

# Variáveis globais (mantém apenas o último QR válido)
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

        # URL que o QR code vai abrir
        url = f"https://www.serranegrablog.com/erro?id={unique_id}"

        # Cria o QR Code em memória
        img = qrcode.make(f"https://qr-api-1-63iq.onrender.com/validar?id={unique_id}")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Retorna a imagem PNG
        return Response(buffer.getvalue(), mimetype='image/png')

    except Exception as e:
        return f"Erro ao gerar QR: {e}"

@app.route('/validar')
def validar_qr():
    global current_qr, qr_created_at

    codigo = request.args.get("id")

    # Nenhum QR foi gerado ainda
    if not current_qr or not qr_created_at:
        return "<h3 style='color:red;'>❌ Nenhum QR ativo no momento.</h3>", 403

    # Se passou de 1 minuto, expira
    if time.time() - qr_created_at > EXPIRATION_TIME:
        return "<h3 style='color:red;'>⏰ QR Code expirado!</h3>", 403

    # Se o código for o atual
    if codigo == current_qr:
        tempo_restante = int(EXPIRATION_TIME - (time.time() - qr_created_at))
        return f"<h3 style='color:green;'>✅ QR Code válido!</h3><p>Expira em {tempo_restante} segundos.</p>"
    else:
        return "<h3 style='color:red;'>❌ QR Code inválido ou antigo!</h3>", 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


