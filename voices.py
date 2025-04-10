import requests
import os

TTS_SERVER_URL = "http://localhost:5002/api/tts"
AUDIO_FOLDER = "audios"
AUDIO_FILE = "audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)


def call_coqui(text, speaker):
    tts_headers = {"text": text, "speaker-id": speaker, "language-id": "en"}
    tts_response = requests.post(TTS_SERVER_URL, headers=tts_headers)

    

    if tts_response.status_code == 200:
        path = os.path.join(AUDIO_FOLDER, f"{AUDIO_FILE}{speaker}.wav")
        with open(path, "wb") as f:
            f.write(tts_response.content)
    else:
        print(f"TTS Error: {tts_response.status_code} - {tts_response.text}")


speakers = ['Claribel Dervla', 'Daisy Studious', 'Gracie Wise', 'Tammie Ema', 'Alison Dietlinde', 'Ana Florence', 'Annmarie Nele', 'Asya Anara', 'Brenda Stern', 'Gitta Nikolina', 'Henriette Usha', 'Sofia Hellen', 'Tammy Grit', 'Tanja Adelina', 'Vjollca Johnnie', 'Andrew Chipper', 'Badr Odhiambo', 'Dionisio Schuyler', 'Royston Min', 'Viktor Eka', 'Abrahan Mack', 'Adde Michal', 'Baldur Sanjin', 'Craig Gutsy', 'Damien Black', 'Gilberto Mathias', 'Ilkin Urbano', 'Kazuhiko Atallah', 'Ludvig Milivoj', 'Suad Qasim', 'Torcull Diarmuid', 'Viktor Menelaos', 'Zacharie Aimilios', 'Nova Hogarth', 'Maja Ruoho', 'Uta Obando', 'Lidiya Szekeres', 'Chandra MacFarland', 'Szofi Granger', 'Camilla Holmström', 'Lilya Stainthorpe', 'Zofija Kendrick', 'Narelle Moon', 'Barbora MacLean', 'Alexandra Hisakawa', 'Alma María', 'Rosemary Okafor', 'Ige Behringer', 'Filip Traverse', 'Damjan Chapman', 'Wulf Carlevaro', 'Aaron Dreschner', 'Kumar Dahl', 'Eugenio Mataracı', 'Ferran Simen', 'Xavier Hayasaka', 'Luis Moray', 'Marcos Rudaski']

text = "TTS is a Voice generation model that lets you clone voices into different languages by using just a quick 6-second audio clip. There is no need for an excessive amount of training data that spans countless hours."

for x in speakers:
    call_coqui(text, x)
