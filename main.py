# main.py
from flask import Flask, Response, request
import qrcode
import io
import random
import string
import os

app = Flask(__name__)

def make_random_code(n=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

@app.route("/qr")
def generate_qr():
    # Gera um código aleatório único
    unique_code = make_random_code(8)

    # Se quiser que a URL alvo venha via query param use:
    # target = request.args.get("u", "https://www.serranegrablog.com")
    # Neste exemplo usamos o domínio fixo:
    base_url = "https://www.serranegrablog.com/erro"
    qr_url = f"{base_url}?id={unique_code}"

    # Gera o QR Code (PIL image)
    img = qrcode.make(qr_url)

    # Converte para bytes PNG
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Retorna como imagem PNG (sem cache para garantir renovação)
    headers = {
        "Content-Type": "image/png",
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
    }
    return Response(buffer.read(), headers=headers)

# Porta padrão (alguns PaaS definem PORT via env)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
