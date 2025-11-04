from flask import Flask, Response, request
import qrcode
import io
import random
import string
import os
import time
import json

app = Flask(__name__)

EXPIRATION_TIME = 60  # segundos (1 minuto)
DATA_FILE = "qr_data.json"  # arquivo simples para guardar o último QR

def save_qr_data(code):
    data = {"code": code, "timestamp": time.time()}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_qr_data():
    if not os.path.exists(DATA_FILE):
        return None, None
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return data.get("code"), data.get("timestamp")

@app.route('/')
def home():
    return "<h2>Servidor de QR Codes ativo ✅</h2><p>Use /qr para gerar um novo QR code.</p>"

@app.route('/qr')
def generate_qr():
    try:
        # Gera um código único
        unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        save_qr_data(unique_id)  # salva no arquivo

        # Monta o link de validação
        url = f"https://qr-api-vl7v.onrender.com/validar?id={unique_id}"

        # Gera o QR Code
        img = qrcode.make(url)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return Response(buffer.getvalue(), mimetype='image/png')

    except Exception as e:
        return f"Erro ao gerar QR: {e}"

@app.route('/validar')
def validar_qr():
    codigo = request.args.get("id")
    last_code, code_timestamp = load_qr_data()

    if not last_code or not code_timestamp:
        return "<h3 style='color:red;'>❌ Nenhum QR ativo no momento.</h3>", 403

    # Verifica se expirou
    if time.time() - code_timestamp > EXPIRATION_TIME:
        return "<h3 style='color:red;'>⏰ QR Code expirado (tempo esgotado)!</h3>", 403

    if codigo == last_code:
        tempo_restante = int(EXPIRATION_TIME - (time.time() - code_timestamp))
        return f"<h3 style='color:green;'>✅ QR Code válido!</h3><p>Expira em {tempo_restante} segundos.</p>"
    else:
        return "<h3 style='color:red;'>❌ QR Code inválido ou antigo!</h3>", 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




