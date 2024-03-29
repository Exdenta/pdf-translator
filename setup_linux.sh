sudo apt-get install poppler-utils
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-lang

python3 -m virtualenv --python=python3.11 venv311
source venv311/bin/activate

pip install -r requirements.txt

