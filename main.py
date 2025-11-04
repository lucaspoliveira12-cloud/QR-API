from flask import Flask, send_file
import qrcode
from PIL import Image
import io
import random
import string

app = Flask(__name__)

@app.route('/')
def gerar_qr():
    # Gera um código aleatório (para que o QR seja sempre único)
    codigo = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # Define o link de destino
    url = f"https://www.serranegrablog.com/?id={codigo}"

    # Cria o QR Code com alta correção de erro (para suportar logo)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Cria imagem do QR
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Adiciona a logo (deve estar na mesma pasta)
    logo_path = "logo.png"  # mantenha esse nome
    try:
        logo = Image.open(logo_path)
        # Redimensiona a logo
        basewidth = 100
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

        # Centraliza a logo no QR
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
    except Exception as e:
        print("Logo não encontrada ou inválida:", e)

    # Retorna o QR como imagem PNG
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



