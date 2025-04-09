import requests


TTS_SERVER_URL = "http://localhost:5002/api/tts"

def call_coqui(text, i):
    #tts_headers = {"text": text, "speaker-id": str(i)}
    #tts_response = requests.post(TTS_SERVER_URL, headers=tts_headers)

    headers = {
        "text": text,
        "speaker-id": str(i)
    }

    response = requests.post(TTS_SERVER_URL, headers=headers)

    if tts_response.status_code == 200:
        path = os.path.join(AUDIO_FOLDER, f"{AUDIO_FILE}{i}.wav")
        with open(path, "wb") as f:
            f.write(tts_response.content)
    else:
        print(f"TTS Error: {tts_response.status_code} - {tts_response.text}")


call_coqui("Hello this is a test. I am voice one", 1)
#call_coqui("Hello this is a test. I am voice two", 2)
#call_coqui("Hello this is a test. I am voice three", 3)
#call_coqui("Hello this is a test. I am voice four", 4)
#call_coqui("Hello this is a test. I am voice five", 5)
#call_coqui("Hello this is a test. I am voice six", 6)
#call_coqui("Hello this is a test. I am voice seven", 7)
