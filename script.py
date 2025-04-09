import subprocess
import threading
import requests
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
import time
import queue
import itertools
import sys
import re

# Configurations
API_URL = "http://localhost:8081/v1/chat/completions"
MODEL_NAME = "mistral-small-25b-2504-Q6_k_L"
HEADERS = {"Content-Type": "application/json"}
TTS_SERVER_URL = "http://localhost:5002/api/tts"
TEMP_AUDIO_FILE = "recorded.wav"
AUDIO_FOLDER = "audios"
AUDIO_FILE = "audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

messages = [
    {"role": "system", "content": "You are a helpful and friendly AI assistant. You are not allowed to use emojis, or any symbols exept '.'"}
]

is_processing = False
audio_counter = 0

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_endevent(pygame.USEREVENT)


def animate_dots(message="Processing"):
    for dot_count in itertools.cycle(range(4)):
        if not is_processing:
            break
        dots = "." * dot_count
        sys.stdout.write(f"\r{message}{dots}   ")
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write("\r" + " " * 40 + "\r")
    sys.stdout.flush()

def record_audio():
    print("[INFO] Press ENTER to start recording.")
    input()
    print("[INFO] Recording... Press ENTER to stop.")
    process = subprocess.Popen([
    "ffmpeg", "-y", "-f", "alsa", "-i", "default",
    "-ac", "1", "-ar", "16000", TEMP_AUDIO_FILE
    ], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    input()  # Wait for second Enter
    process.terminate()
    process.wait()
    print("[INFO] Recording stopped.")
    time.sleep(0.5)

def transcribe_audio():
    try:
        
        txt_file = TEMP_AUDIO_FILE + ".txt"
        if os.path.exists(txt_file):
            os.remove(txt_file)


        result = subprocess.run([
            "./whisper.cpp/build/bin/whisper-cli",  # adjust if needed
            "-m", "./whisper.cpp/models/ggml-base.en.bin",
            "-f", TEMP_AUDIO_FILE,
            "-otxt"
        ], capture_output=True, text=True)

        
        if os.path.exists(txt_file):
            with open(txt_file, "r") as f:
                text = f.read().strip()
            #os.remove(txt_file)
            return text
        else:
            print("Transcription failed.")
            return ""
    except Exception as e:
        print(f"[ERROR] Transcription error: {e}")
        return ""

def play_audio(file_path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()
    while pygame.mixer.get_busy():
        time.sleep(0.1)

def run_pipeline():
    global is_processing

    while True:
        record_audio()
        if is_processing:
            continue

        is_processing = True
        transcribed = transcribe_audio()
        print(f"[User] {transcribed}")

        messages.append({"role": "user", "content": transcribed})

        try:
            response = requests.post(API_URL, json={
                "model": MODEL_NAME,
                "messages": messages,
                "temperature": 0.7
            }, headers=HEADERS)

            reply = response.json()["choices"][0]["message"]["content"].strip()
            clean_reply = reply.replace("\n", " ").replace("\r", "")
            print(f"\nAI: {clean_reply}")

            tts(clean_reply)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            is_processing = False

def call_coqui(text, i):
    tts_headers = {"text": text}
    tts_response = requests.post(TTS_SERVER_URL, headers=tts_headers)

    if tts_response.status_code == 200:
        path = os.path.join(AUDIO_FOLDER, f"{AUDIO_FILE}{i}.wav")
        with open(path, "wb") as f:
            f.write(tts_response.content)
    else:
        print(f"TTS Error: {tts_response.status_code} - {tts_response.text}")
    

def generateSentences(sentences):
    for index, sentence in enumerate(sentences):
        call_coqui(sentence,index + 1)

def play(file):
    path = os.path.join(AUDIO_FOLDER, f"{file}.wav")
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def audio_event_loop(length):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                os.remove(os.path.join(AUDIO_FOLDER, f"{AUDIO_FILE}{audio_counter}.wav"))
                x = on_audio_end(length)
                if x :
                    return
        time.sleep(0.1)

def on_audio_end(length):
    global audio_counter
    audio_counter += 1
    if(audio_counter == length):
        return True
    
    while(True):
        if os.path.exists(os.path.join(AUDIO_FOLDER, f"{AUDIO_FILE}{audio_counter}.wav")):
            break
    
    play(AUDIO_FILE + str(audio_counter))
    return False

def tts(input):
    sentences = re.split(r'(?<=[.!?])\s+', input)
    length = len(sentences)
    global audio_counter
    audio_counter = 0
    call_coqui(sentences.pop(0), 0)
    play(AUDIO_FILE + str(0))
    t = threading.Thread(target=generateSentences, args=(sentences,), daemon=True)
    t.start()
    audio_event_loop(length)



# Start the main loop
run_pipeline()
