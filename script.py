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

messages = [
    {"role": "system", "content": "You are a helpful and friendly AI assistant. You are not allowed to use emojis, or any symbols exept '.'"}
]

is_processing = False


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

            # TTS
            tts_headers = {"text": clean_reply, "style_wav": "{rate: 4}"}
            tts_response = requests.post(TTS_SERVER_URL, headers=tts_headers)

            if tts_response.status_code == 200:
                with open("output.wav", "wb") as f:
                    f.write(tts_response.content)
                play_audio("output.wav")
            else:
                print(f"TTS Error: {tts_response.status_code} - {tts_response.text}")

            messages.append({"role": "assistant", "content": clean_reply})

        except Exception as e:
            print(f"Error: {e}")
        finally:
            is_processing = False


# Start the main loop
run_pipeline()
