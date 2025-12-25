from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from googletrans import Translator
import base64
import io

app = Flask(__name__)

# Supported languages
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Urdu": "ur"
}

@app.route("/")
def index():
    return render_template("index.html", languages=LANGUAGES)

@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text")
    target_lang = request.form.get("output_language")

    if not text or not target_lang:
        return jsonify({"error": "Missing text or language"}), 400

    # Translate text
    translator = Translator()
    translated_text = translator.translate(text, dest=target_lang).text

    # Text to speech
    tts = gTTS(text=translated_text, lang=target_lang)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)

    # Convert to base64
    audio_base64 = base64.b64encode(audio_fp.read()).decode("utf-8")

    return jsonify({"audio": audio_base64})

if __name__ == "__main__":
    app.run(debug=True)

