import os
from flask import Flask, request, jsonify
from elevenlabs import generate, play, save, set_api_key
from dotenv import load_dotenv

# .env laden
load_dotenv()

# API-Key und Voice-IDs
set_api_key(os.getenv("ELEVENLABS_API_KEY"))
VOICE_ID_MEISTER = os.getenv("VOICE_ID_MEISTER")
VOICE_ID_NARION = os.getenv("VOICE_ID_NARION")

# Flask App
app = Flask(__name__)

def generate_speech(text, speaker):
    if speaker == "meister":
        voice_id = VOICE_ID_MEISTER
    elif speaker == "narion":
        voice_id = VOICE_ID_NARION
    else:
        return False

    try:
        audio = generate(text=text, voice=voice_id)
        save(audio, "output.mp3")
        return True
    except Exception as e:
        print("❌ Fehler bei der Sprachausgabe:", e)
        return False

@app.route("/")
def home():
    return jsonify({"message": "Meister-GPT API läuft. Verwende POST /sprich mit JSON {'prompt': '...', 'speaker': 'meister' oder 'narion'}"})

@app.route("/sprich", methods=["POST"])
def sprich():
    data = request.get_json()
    prompt = data.get("prompt", "")
    speaker = data.get("speaker", "").lower()

    if not prompt or speaker not in ["meister", "narion"]:
        return jsonify({"error": "Ungültiger Prompt oder Sprechername fehlt"}), 400

    success = generate_speech(prompt, speaker)
    if success:
        return jsonify({"status": "ok", "message": f"Sprachausgabe für {speaker} erzeugt."})
    else:
        return jsonify({"status": "fehler", "message": "Sprachausgabe fehlgeschlagen."}), 500

if __name__ == "__main__":
    app.run(debug=True)