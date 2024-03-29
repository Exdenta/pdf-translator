brew install poppler
brew install tesseract
brew install tesseract-lang

python3 -m virtualenv --python=python3.11 venv311
source venv311/bin/activate

pip install -r requirements.txt

