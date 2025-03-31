from flask import Flask, request, jsonify
import logging
import uuid

app = Flask(__name__)

logging.basicConfig(filename='glocken.log', level=logging.INFO)

@app.route('/')
def home():
    return 'Glockenmeter läuft!'

@app.route('/sprich', methods=['POST'])
def sprich():
    prompt = request.json.get('prompt', '')
    logging.info(f"Empfangenes Prompt: {prompt}")

    # Simulierte Antwort (in echt würde GPT & ElevenLabs hier eingebunden)
    audio_url = f"https://dummy-audio-url.com/audio-{uuid.uuid4()}.mp3"
    logging.info(f"Audio erzeugt: {audio_url}")

    return jsonify({ "audio_url": audio_url })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
