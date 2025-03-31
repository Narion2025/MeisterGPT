import os
from flask import Flask, request, send_file, jsonify
import requests

app = Flask(__name__)

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY", "sk_00b61c58397f0eff7e60831ee861673dff1b65b25b8e31c4")
VOICE_ID = os.getenv("VOICE_ID", "ur39JFtQKjsZgv7ZF8CO")
AUDIO_FILE = "output.mp3"

def generate_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        with open(AUDIO_FILE, "wb") as f:
            f.write(response.content)
        return True
    else:
        print("Fehler bei ElevenLabs:", response.text)
        return False

@app.route("/sprich", methods=["POST"])
def sprich():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Kein Prompt übergeben"}), 400
    success = generate_speech(prompt)
    if success:
        return send_file(AUDIO_FILE, mimetype="audio/mpeg")
    else:
        return jsonify({"error": "Text-to-Speech fehlgeschlagen"}), 500

@app.route("/", methods=["GET"])
def info():
    return "Meister-GPT API läuft. Verwende POST /sprich mit JSON {"prompt": "..."}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)