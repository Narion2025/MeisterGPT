from flask import Flask, request, jsonify
import os
import requests  # Import für HTTP-Anfragen
from elevenlabs import generate, save, set_api_key

app = Flask(__name__)

# API-Schlüssel aus Umgebungsvariablen laden
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
set_api_key(ELEVEN_API_KEY)

VOICE_ID = os.getenv("VOICE_ID", "6ElpBsQOx7eBvS5X6bSg")  # Meister
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

    try:
        success = generate_speech(prompt)
        if success:
            return jsonify({"status": "OK", "message": "Audio generiert", "file": AUDIO_FILE}), 200
        else:
            return jsonify({"error": "Text-to-Speech fehlgeschlagen"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)