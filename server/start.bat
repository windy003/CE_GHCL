@echo off

echo Setting up Python virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo Starting GitHub Code Counter Server...
python app.py

pause