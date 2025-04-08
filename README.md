# stt-llm-tts_demo

## Virtual Python Environment
Create:
- `python -m venv venv`

Enter:
- `source venv/bin/activate`

Install packages:
- `pip install requests`

Exit: 
- `deactivate`


## Run TTS:
- `sudo docker run --rm -it -p 5002:5002 --entrypoint /bin/bash ghcr.io/coqui-ai/tts-cpu`
- `python3 TTS/server/server.py --list_models` to list all models
- `python3 ~/TTS/server/server.py --model_name tts_models/en/ljspeech/vits--neon`
- start tts.py


## Llama cpp server

- `localhost:8080`/ `localhost:8081`
- `ssh eowyn`

## Build whisper-cpp

- `cd whisper.cpp`
- `cmake -B build -DGGML_VULKAN=1`
- `cmake --build build -j --config Release`
