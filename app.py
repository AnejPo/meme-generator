from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

app = Flask(__name__)

# mapa za generirane meme
OUTPUT_DIR = "static/memes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("image")
        top_text = request.form.get("top_text", "").upper()
        bottom_text = request.form.get("bottom_text", "").upper()

        if not uploaded_file:
            return "Ni slike!", 400

        # Odpri sliko
        img = Image.open(uploaded_file.stream).convert("RGB")
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Font (dynamic size)
        font_size = int(width / 10)
        font_path = os.path.join(os.path.dirname(__file__), "fonts/Impact.ttf")
        font = ImageFont.truetype(font_path, font_size)


        # Funkcija za izris teksta z obrisom
        def draw_text(position, text):
            x, y = position
            outline = int(font_size / 15)  # debelina obrisa

            # Obris
            for dx in range(-outline, outline + 1):
                for dy in range(-outline, outline + 1):
                    draw.text((x + dx, y + dy), text, font=font, fill="black")

            # Bela sredina
            draw.text(position, text, font=font, fill="white")

        # ZGORNJI TEKST — sredinsko
        if top_text:
            bbox = draw.textbbox((0, 0), top_text, font=font)
            text_width = bbox[2] - bbox[0]
            top_position = ((width - text_width) / 2, 10)
            draw_text(top_position, top_text)

        # SPODNJI TEKST — sredinsko
        if bottom_text:
            bbox = draw.textbbox((0, 0), bottom_text, font=font)
            text_width = bbox[2] - bbox[0]
            bottom_position = ((width - text_width) / 2, height - bbox[3] - 10)
            draw_text(bottom_position, bottom_text)

        # Shrani generiran meme
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
        output_path = os.path.join(OUTPUT_DIR, filename)
        img.save(output_path)

        # Vrni HTML, ki pokaže sliko
        meme_url = f"/{output_path}"
        return render_template("index.html", meme_url=meme_url)

    return render_template("index.html", meme_url=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
