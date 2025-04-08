# --- whisper.cpp build ---
if [ ! -d "whisper.cpp/build" ]; then
  echo "Building whisper.cpp with Vulkan support..."
  cd whisper.cpp || exit
  cmake -B build -DGGML_VULKAN=1
  cmake --build build -j --config Release
  cd ..
fi


# --- Virtual environment setup ---
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

if [ -z "$VIRTUAL_ENV" ]; then
  echo "Activating"
  source venv/bin/activate
  pip install -r requirements.txt
fi

python script.py