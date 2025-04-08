import re
import threading
import requests
import pygame
import time
import os

TTS_SERVER_URL = "http://localhost:5002/api/tts"

AUDIO_FOLDER = "audios"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

AUDIO_FILE = "audio"


def call_coqui(text, i):
    tts_headers = {"text": text}
    tts_response = requests.post(TTS_SERVER_URL, headers=tts_headers)

    if tts_response.status_code == 200:
        path = os.path.join(AUDIO_FOLDER, f"{AUDIO_FILE}{i}.wav")
        with open(path, "wb") as f:
            f.write(tts_response.content)
    else:
        print(f"TTS Error: {tts_response.status_code} - {tts_response.text}")
    

def generateSentences():
    for index, s in enumerate(sentences):
        call_coqui(s,index + 1)

def play(file):
    path = os.path.join(AUDIO_FOLDER, f"{file}.wav")
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def audio_event_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                x = on_audio_end()
                if x :
                    return
        time.sleep(0.1)

def on_audio_end():
    global counter
    counter += 1
    if(counter == length):
        return True
    
    while(True):
        if os.path.exists(os.path.join(AUDIO_FOLDER, f"{AUDIO_FILE}{counter}.wav")):
            break
    
    play(AUDIO_FILE + str(counter))
    return False

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_endevent(pygame.USEREVENT)


input = "The sun was setting behind the hills, casting a golden glow over the valley. Birds chirped softly as the evening breeze rolled in. Emily sat on the porch, sipping her tea and watching the sky change colors. It had been a long day, but moments like this made it all worthwhile. She smiled, thinking about the adventures tomorrow might bring."
sentences = re.split(r'(?<=[.!?])\s+', input)
length = len(sentences)
counter = 0

print(sentences)
call_coqui(sentences.pop(0), 0)
play(AUDIO_FILE + str(0))


t = threading.Thread(target=generateSentences, daemon=True)
t.start()

audio_event_loop()

t.join()






