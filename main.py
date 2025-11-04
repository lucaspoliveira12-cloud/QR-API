# main.py
from flask import Flask, send_file, Response
import qrcode
from PIL import Image
import io
import random
import string
import os   # <--- IMPORT ESSENCIAL ADICIONADO

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>Servidor de QR Codes ativo ✅</h2>"

@app.route('/qr')
def generate_qr():
    try:
        # Gera um código único a cada carregamento
        unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        url = f"https://www.serranegrablog.com/?id={unique_id}"

        # Cria o QR Code com alta correção (necessário para colocar logo)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Gera a imagem do QR
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Tenta abrir e colar a logo (logo.png deve estar na mesma pasta)
        logo_path = "logo.png"
        try:
            logo = Image.open(logo_path)
            # Redimensiona a logo proporcionalmente (base 100 px)
            basewidth = 100
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            # Use Image.LANCZOS se sua versão do Pillow suportar
            try:
                logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            except AttributeError:
                logo = logo




