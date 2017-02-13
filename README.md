# Computes OCR output statistics against a German dictionary

## Prepare

Please, use Python 3.

First, initialize virtual environment
```
virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Then, download `german.7z` into `dictionary/` directory and unpack it
```
mkdir dictionary
cd dictionary/
wget https://downloads.sourceforge.net/project/germandict/german.7z
7zr e german.7z
cd ..
```

Next, copy all OCR `*.txt` files into `ocr-hlsl/` directory
```
mkdir ocr-hlsl
cp ~/Downloads/ocr-hlsl/*.txt ocr-hlsl/
```

Last, copy all OCR `*.xml` files into `ocr-inno/` directory
```
mkdir ocr-inno
cp ~/Downloads/ocr-inno/*.xml ocr-inno/
```

## Running
```
python main.py
```
