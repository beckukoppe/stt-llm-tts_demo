python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd whisper.cpp
cmake -B build -DGGML_VULKAN=1
cmake --build build -j --config Release