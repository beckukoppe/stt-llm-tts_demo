
if [ -d "audios/" ]; then
  echo "Removing audios..."
  rm -rf 'audios/'
fi

# --- whisper.cpp build ---
if [ ! -d "whisper.cpp/build" ]; then
  echo "Building whisper.cpp with Vulkan support..."
  cd whisper.cpp || exit
  cmake -B build -DGGML_VULKAN=1
  cmake --build build -j --config Release
  cd ..
fi

if [ ! -f "whisper.cpp/models/ggml-base.en.bin" ]; then
  ./whisper.cpp/models/download-ggml-model.sh base.en
fi

# --- Virtual environment setup ---
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

if [ -z "$VIRTUAL_ENV" ]; then
  echo "Activating virtual environment..."
  source venv/bin/activate
  pip install -r requirements.txt
fi

clear

python script.py





