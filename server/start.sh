#!/bin/bash

echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Starting GitHub Code Counter Server..."
python app.py