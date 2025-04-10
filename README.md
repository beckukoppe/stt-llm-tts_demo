# stt-llm-tts_demo

## Virtual Python Environment
Create:
- `python -m venv venv`

Enter:
- `source venv/bin/activate`

Install packages:
- `pip install -r requirements.txt`

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

## xtts

docker run --rm -it -p 5002:5002 --gpus all --entrypoint /bin/bash ghcr.io/coqui-ai/tts

--use_cuda true



tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 --list_speaker

python3 TTS/server/server.py --model_name tts_models/multilingual/multi-dataset/xtts_v2 --config_path /root/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/config.json --model_path /root/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/



['Claribel Dervla', 'Daisy Studious', 'Gracie Wise', 'Tammie Ema', 'Alison Dietlinde', 'Ana Florence', 'Annmarie Nele', 'Asya Anara', 'Brenda Stern', 'Gitta Nikolina', 'Henriette Usha', 'Sofia Hellen', 'Tammy Grit', 'Tanja Adelina', 'Vjollca Johnnie', 'Andrew Chipper', 'Badr Odhiambo', 'Dionisio Schuyler', 'Royston Min', 'Viktor Eka', 'Abrahan Mack', 'Adde Michal', 'Baldur Sanjin', 'Craig Gutsy', 'Damien Black', 'Gilberto Mathias', 'Ilkin Urbano', 'Kazuhiko Atallah', 'Ludvig Milivoj', 'Suad Qasim', 'Torcull Diarmuid', 'Viktor Menelaos', 'Zacharie Aimilios', 'Nova Hogarth', 'Maja Ruoho', 'Uta Obando', 'Lidiya Szekeres', 'Chandra MacFarland', 'Szofi Granger', 'Camilla Holmström', 'Lilya Stainthorpe', 'Zofija Kendrick', 'Narelle Moon', 'Barbora MacLean', 'Alexandra Hisakawa', 'Alma María', 'Rosemary Okafor', 'Ige Behringer', 'Filip Traverse', 'Damjan Chapman', 'Wulf Carlevaro', 'Aaron Dreschner', 'Kumar Dahl', 'Eugenio Mataracı', 'Ferran Simen', 'Xavier Hayasaka', 'Luis Moray', 'Marcos Rudaski']

